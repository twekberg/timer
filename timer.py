"""
Brings up a small gui that has two button. One to add a new row and one to stop.
"""

#

"""
TODO:
Make this work when the day changes.
--------------------DONE--------------------
Wrote report that details N days of data, starting with today.

Implemented hide. Was able to unhide and retain the time value.

Removed New Day since it isn't really needed.
Need a .config file of some sort to
  auto-save interval
Write callback to Save to
  Load today's JSON file, if it exists.
  Store button.text and timedelta

Use frame.after(1000, new_second)`
  calculate new timedelta and store in widget_2.text
    datetime.now() - start_date
When exiting store data as if the user clicked the save button.

When loading, look for today's data.

set self.active_row = one of the class instances.

Define a class for the row detail
  button
  label
  sel_checkbox # Checkbutton for user to delete.
  timedelta
  start_time - when the button was last clicked

Changed the buttons to
  Add    Hide
  Pause  Save
  Exit   New day    # resets timedeltas to 0

Moved buttons to the top.

Redid action button creation to not use new_row. It's too complicated and we don't need to save them anyway.

Change add new data button to allow one to enter a value for the new button.
"""


import tkinter as tk
from tkinter import simpledialog, filedialog
from datetime import datetime, timedelta
import os
import os.path
import json


class App(tk.Frame):

    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root
        self.button_frame = tk.Frame(self.root)
        self.button_frame.grid()
        self.button_off = None
        self.label_off = None
        self.active_row = None

        self.row_detail_list = []

        # Look for a JSON file for today.
        today_filename = self.get_day_data_path()
        if os.path.isfile(today_filename):
            # Found a file for today.
            with open(today_filename) as tf:
                today_data = json.load(tf)
        else:
            # Look in the past for a data file and use those categories, with time=0
            # as a basis for today's categories. Look back at most 100 days. This
            # many days accounts for a long vacation.
            for day in range(1, 101):
                day_filename = self.get_day_data_path(day)
                if os.path.isfile(day_filename):
                    # Found a file for this day.
                    with open(day_filename) as df:
                        day_data = json.load(df)
                    today_data = [ {'category': d['category'], 'time': '0:00:00'} for d in day_data]
                    break
            else:
                today_data = []

        self.config_setup()

        menubar = tk.Menu(self.button_frame)
        menubar.add_command(label="Add", command=self.add_new_data)
        menubar.add_command(label="Hide", command=self.hide)
        menubar.add_command(label="Del", command=self.delete_category)
        menubar.add_command(label="Pause", command=self.pause)
        menubar.add_command(label="Save", command=self.save)
        menubar.add_command(label="Report", command=self.report)
        menubar.add_command(label="Exit", command=self.exit)
        menubar.add_command(label="Help", command=self.help)
        root.config(menu=menubar)

        for (i, row) in enumerate(today_data):
            rd = RowDetail(row['category'], row['time'], self.button_frame, self.category_clicked)
            self.row_detail_list.append(rd)
            self.row_detail_list[i].frame.grid(row=i)
            if not self.button_off:
                self.button_off = rd.button.cget('background')
            if not self.label_off:
                self.label_off = rd.label.cget('background')


    def hide(self):
        """
        Hide rows selected by the user.
        """
        hide_us = []
        for rd in self.row_detail_list:
            if rd.cb_var.get():
                hide_us.append(rd)
        if hide_us:
            # Make sure the category/time values are in the JSON file before we remove them
            self.save()

            for rd in hide_us:
                self.row_detail_list.remove(rd)
            self.refresh_display()
        else:
            tk.messagebox.showinfo("Missing", "Click the checkbox next to the category you want to hide.")


    def delete_category(self):
        delete_us = []
        exclude_list = []
        for rd in self.row_detail_list:
            if rd.cb_var.get():
                delete_us.append(rd)
                exclude_list.append(rd.button.cget('text'))
                
        if delete_us:
            # Remove them from the GUI and then save.
            # This will retain any hidden categories, but delete these.
            for rd in delete_us:
                self.row_detail_list.remove(rd)
            self.refresh_display()
            self.save(exclude_list)
        else:
            tk.messagebox.showinfo("Missing", "Click the checkbox next to the category you want to delete.")


    def get_day_data_path(self, days_ago=0):
        """
        Get the data path for today, or for a day in the past.
        """
        home = os.environ.get('USERPROFILE').replace('\\', '/')
        self.data_dir= os.path.join(home, 'TimeData')
        if not os.path.isdir(self.data_dir):
            mkdir(self.data_dir)
        today_filename = os.path.join(
            self.data_dir,
            (datetime.now()-timedelta(days=days_ago)).strftime('%Y-%m-%d.json'))
        return today_filename


    def config_setup(self):
        # Look for a config file, also JSON
        config_file = os.path.join(self.data_dir, 'time_data_config.json')
        if os.path.isfile(config_file):
            self.auto_save_interval = None;
            with open(config_file) as jin:
                config = json.load(jin)
                self.auto_save_interval = config['auto_save_interval']
        else:
            self.auto_save_interval = 60 # minutes
            # Default to every 60 minutes, but save it in the config file so the
            # user can change it.
            config = {'auto_save_interval': self.auto_save_interval}
            with open(config_file, 'w') as jout:
                json.dump(config, jout, sort_keys=True,
                      indent=4, separators=(',', ': '))
        if self.auto_save_interval:
            self.button_frame.after(self.auto_save_interval * 60 * 1000, self.auto_save)


    def pause(self):
        for rd in self.row_detail_list:
            rd.button.config(background=self.button_off)
            rd.label.config(background=self.label_off)
        self.active_row = None


    def auto_save(self):
        self.save()
        self.button_frame.after(self.auto_save_interval * 60 * 1000, self.auto_save)


    def save(self, exclude_list=[], days_ago=0):
        # Keep the times for categories that have been hidden.
        today_filename = self.get_day_data_path(days_ago)
        if os.path.isfile(today_filename):
            with open(today_filename) as tf:
                today_data = json.load(tf)
        else:
            today_data = []
        for rd in self.row_detail_list:
            for td in today_data:
                if td['category'] == rd.category:
                    # Existing category needs updating.
                    td['time'] = rd.time
                    break
            else:
                # New category, not stored in JSON file.
                td = dict()
                td['category'] = rd.category
                td['time'] = rd.time
                today_data.append(td)

        for delete_me in exclude_list:
            for td in today_data:
                 if td['category'] == delete_me:
                     today_data.remove(td)
                     break
        today_data.sort(key=lambda d: d['category'].lower())
        with open(today_filename, 'w') as jout:
            json.dump(today_data, jout, sort_keys=True,
                      indent=4, separators=(',', ': '))


    def report(self):
        report_filename = filedialog.asksaveasfilename(initialdir = self.data_dir.replace('C:','/cygdrive/c'),
                                                          title = "Write Report",
                                                          filetypes = (("text files","*.txt"),
                                                                       ("all files","*.*")))
        if not report_filename:
            return
        with open(report_filename, 'w') as rep_o:
            print('Time Data report written', datetime.now(), file=rep_o)
            for day in range(7):
                day_filename = self.get_day_data_path(day)
                if os.path.isfile(day_filename):
                    print('', file=rep_o)
                    with open(day_filename) as df:
                        day_data = json.load(df)
                    print('Report for ', day_filename.rsplit('/', maxsplit=1)[1], file=rep_o)
                    for dd in day_data:
                        print('  %s: %s' % (dd['category'], dd['time']), file=rep_o)



    def exit(self):
        self.save()
        root.quit()
        root.destroy()


    def help(self):
        tk.messagebox.showinfo("Help", """Add - add a new or previously existing category.
Hide - click on the checkbox for a category to hide, then click Hide. Any time data is retained in the file.
Del - click on the checkbox for a category to delete, then click Del. These categories are removed from the file.
Pause - stop the current timer.
Save - save the timers now.
Report - generate a report for the past 7 days. You specify where to save it.
Exit - save the timers and exit this program.""")


    def category_clicked(self, b, l):
        """
        The user clicked on one of the dategory buttons.
        """
        for rd in self.row_detail_list:
            frame = rd.frame
            button = rd.button
            label = rd.label
            if button == b:
                # Change the button's bg state, on->off, off->on
                if self.button_off == b.cget('background'):
                    self.active_row = rd
                    button.config(background='pale green')
                    secs = self.hms_to_seconds(label.cget('text'))
                    # Only one is active at a time, so might as well store start_time here.
                    self.start_time = datetime.now() - timedelta(seconds=secs)
                    frame.after(1000, self.process_next_second)
                else:
                    self.active_row = None
                    button.config(background=self.button_off)
                    label.config(background=self.button_off)
            else:
                button.config(background=self.button_off)
                label.config(background=self.label_off)


    def hms_to_seconds(self, s):
        """
        Convert HH:MM:SS to seconds.
        """
        dt = datetime.strptime(s, '%H:%M:%S')
        return int(timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second).total_seconds())


    def seconds_to_hms(self, secs):
        """
        Convert seconds to HH:MM:SS. The leading 0 on HH is removed.
        """
        return str(timedelta(seconds = secs))


    def process_next_second(self):
        """
        Advanced to the next second.
        Record and advance one more second.
        """
        self.check_day_advance()
        rd = self.active_row
        if not rd:
            # Paused when we still have the 'after' method active.
            # Now that it is not active so we do nothing.
            return
        secs = int((datetime.now() - self.start_time).total_seconds())
        time = self.seconds_to_hms(secs)
        rd.time = time
        rd.label.config(text=time)
        rd.frame.after(1000, self.process_next_second)


    def check_day_advance(self):
        """
        Check to see if we have moved on to another day.
        """
        days_ago = datetime.now().toordinal() - self.start_time.toordinal()
        if days_ago:
            # New day. Save data for the old day.
            self.save(days_ago = days_ago)
            self.start_time = datetime.now()
            # Reset all counters back to 0:00:00.
            for rd in self.row_detail_list:
                rd['time'] = '0:00:00'
            self.refresh_display()


    def add_new_data(self):
        """
        Add a new category
        """
        category = self.get_input("New Category", "New category")
        if not category:
            return

        # Check for duplicates.
        for rd in self.row_detail_list:
            if rd.category == category:
                tk.messagebox.showinfo("Duplicate", "That category is already defined.")
                return

        # If this category is already in the current JSON file, then it was hidden and
        # is now being brought back.
        today_filename = self.get_day_data_path()
        if os.path.isfile(today_filename):
            with open(today_filename) as tf:
                today_data = json.load(tf)
        else:
            today_data = []
        initial_time = '0:00:00'
        for td in today_data:
            if td['category'] == category:
                initial_time = td['time']
                break
                
        rd = RowDetail(category, initial_time, self.button_frame, self.category_clicked)
        self.row_detail_list.insert(0, rd)
        self.refresh_display()


    def refresh_display(self):
        """
        The row_detail_list has changed. Refresh that part of the display.
        """
        for widget in self.button_frame.children.values():
            widget.grid_forget() 

        for (i, rd) in enumerate(self.row_detail_list):
            rd.frame.grid(row=i)


    def get_input(self, title, prompt):
        return simpledialog.askstring(title, prompt)

class RowDetail():
    """
    Holds all of the detail for a row.
    """
    def __init__(self, category, time, parent, command_fun):
        """
        category - text for the category button
        time - text for the time label
        parent - parent for the GUI
        command_fun - function to call when the button is clicked. The aruments are
            the category button and time label.
        """
        self.category = category
        self.time = time
        self.frame = tk.Frame(parent)
        self.cb_var = tk.IntVar()
        self.cb = tk.Checkbutton(self.frame, variable=self.cb_var)
        self.button = tk.Button(self.frame, text=self.category)
        self.label = tk.Label(self.frame, text=time)
        command = lambda: command_fun(self.button, self.label)
        self.button.config(command=command)
        self.cb.pack(side= tk.LEFT)
        self.button.pack(side= tk.LEFT)
        self.label.pack(side= tk.LEFT)


    # Need when this object is in a list.
    def __repr__(self):
        return self.__str__()


    def __str__(self):
        """
        Display a nice repreentation of a RowDetail object.
        """
        return 'RowDetail(catetory=%s, time=%s)' % (self.category, self.time)


if __name__ == "__main__":
    root = tk.Tk()
    root.title('timer')
    # Position window in the middle display just above the eyeballs.
    # Positioning using +NNN for the Y coordinate didn't work, but -nnn worked fine.
    root.geometry('220x410+3621-564')
    my_app = App(root)
    root.mainloop()
