
.. contents:: Table of Contents

Introduction
============
This program displays a small window with a command bar at the top and timer buttons below that.
One ccan do these commands::

  Add - add a new or previously existing category.
  Hide - click on the checkbox for a category to hide, then click Hide. Any time data is retained in the file.
  Del - click on the checkbox for a category to delete, then click Del. These categories are removed from the file.
  Pause - stop the current timer.
  Save - save the timers now.
  Report - generate a report for the past 7 days. You specify where to save it.
  Exit - save the timers and exit this program.

Each of the bottons has a checkbox, the timer label and an upcounting
timer value. The checkbox is only used to hide or delete timer labels.

To start a timer, just click on the timer label. It will keep counting until another timer label is selected
or the program is exited or paused. The timer labels are sorted when the program is started.


System Requirements
-------------------

These are the requirements to run this program::
  cygwin64
    Download these extra packages from the cygwin site:
      python 3.8
      tkinter
  An X window system server. VcXsrv is recommended. Go here:
      https://sourceforge.net/projects/vcxsrv/files/vcxsrv/
    click on the latest version. Then download an installer and install it.
  Bring up the cygwin64 command line, create a src directory (mkdir src),
    go into it (cd src) and enter this command
      git clone  git@github.com:twekberg/timer.git
    This repo is publically available.

Create A Virtualenv And Install Dependencies
--------------------------------------------

While in the timer subdirectory, run these commands::
  python3.8 -m venv timer-env
  source timer-env/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt


Examples
--------

To run the timer program do this::

  ./timer &

There is a report program. Enter this to see the options::

  ./spend_report.py -h

This report uses timer data stored in c:/Users/YOUR_USERNAME/TimeData.
