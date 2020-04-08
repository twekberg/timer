"""
Brings up a small gui that has two button. One to add a new row and one to stop.
"""

#

"""
TODO:
Implement hide.
Implement new day
Write report that details N days of data, starting with today.
--------------------DONE--------------------
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
from tkinter import simpledialog
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
        today_filename = self.get_today_data_path()
        if os.path.isfile(today_filename):
            with open(today_filename) as tf:
                today_data = json.load(tf)
        else:
            today_data = []

        menubar = tk.Menu(self.button_frame)
        menubar.add_command(label="Add", command=self.add_new_data)
        menubar.add_command(label="Hide", command=lambda: print('Hide'))
        menubar.add_command(label="Pause", command=self.pause)
        menubar.add_command(label="Save", command=self.save)
        menubar.add_command(label="New Day", command=lambda: print('New Day'))
        menubar.add_command(label="Exit", command=self.exit)
        root.config(menu=menubar)

        for (i, row) in enumerate(today_data):
            rd = RowDetail(row['category'], row['time'], self.button_frame, self.category_clicked)
            self.row_detail_list.append(rd)
            self.row_detail_list[i].frame.grid(row=i)
            if not self.button_off:
                self.button_off = rd.button.cget('background')
            if not self.label_off:
                self.label_off = rd.label.cget('background')

        
    def get_today_data_path(self):
        home = os.environ.get('USERPROFILE').replace('\\', '/')
        self.data_dir= os.path.join(home, 'TimeData')
        if not os.path.isdir(self.data_dir):
            mkdir(self.data_dir)
        today_filename = os.path.join(self.data_dir, datetime.now().strftime('%Y-%m-%d.json'))
        return today_filename


    def config_setup(self)
        # Look for a config file, also JSON
        config_file = os.path.join(self.data_dir, 'time_data_config.json')
        if isfile(config_file):
            self.auto_save_interval = None;
            with open(config_file) as jin:
                ccnfig = json.load(jin)
            self.auto_save_interval = config['auto_save_interval']
        else:
            auto_save_interval = 60 # minutes
            config = {'auto_save_interval': auto_save_interval}
            with open(config_file, 'w') as jout:
            json.dump(config, jout, sort_keys=True,
                      indent=4, separators=(',', ': '))
        if self.auto_save_interval:
            self.button_frame.after(self.auto_save_interval * 60, self.save)
        

    def pause(self):
        for rd in self.row_detail_list:
            rd.button.config(background=self.button_off)
            rd.label.config(background=self.label_off)
        self.active_row = None


    def save(self):
        today_filename = self.get_today_data_path()
        l = [{'category': rd.category, 'time': rd.label.cget('text')} for rd in self.row_detail_list]
        l.sort(key=lambda d: d['category'].lower())
        with open(today_filename, 'w') as jout:
            json.dump(l, jout, sort_keys=True,
                      indent=4, separators=(',', ': '))


    def exit(self):
        self.save()
        root.quit()
        root.destroy()


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
                    secs = int(label.cget('text'))
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

                
    def process_next_second(self):
        """
        Advanced to the next second.
        Record and advance one more second.
        """
        rd = self.active_row
        if not rd:
            # Paused when we still have the 'after' method active.
            # Not it is not active so we do nothing.
            return
        secs = int((datetime.now() - self.start_time).total_seconds())
        rd.label.config(text=str(secs))
        rd.frame.after(1000, self.process_next_second)
        

    def add_new_data(self):
        """
        Add a new category
        """
        t = self.get_input("New Category", "New category")
        if not t:
            return
        rd = RowDetail(t, str(0), self.button_frame, self.category_clicked)
        self.row_detail_list.insert(0, rd)

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


if __name__ == "__main__":
    root = tk.Tk() 
    root.geometry('200x300')
    my_app = App(root)
    root.mainloop()
