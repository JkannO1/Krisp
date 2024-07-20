# Krispy
Personal CLI task manager in Python

TL;DR walmart Emacs Orgmode ¯\_(ツ)_/¯
## Features (With nots for devs)
1. Add tasks and sub-tasks infinitely (such tasks are called "Nested Tasks")
2. Record time spend per task/subtask
3. detailed calender view showing deadlines of tasks and events
4. for linux-tards(arch btw)
## Install (windows)
1. clone the repo and open cmd and use this command:
```
pip install colorama
```
3. Create a batch file to run the Python script. Name this file 'krispy.bat' and place it in the default cmd directory that is (C:\Users\name) or what ever you have it to.
4. in the batch file add the following lines:
```
@echo off
python 'path\to\your\script\'Index.py
```
Replace path\to\your\script\Index.py with the actual path to your Index.py file.

4. Add the batch file's directory to your system's PATH (if it's not already in the PATH):
    Right-click on 'This PC' or 'Computer' on your desktop or in File Explorer, and select 'Properties'.
    Click on 'Advanced system settings'.
    Click on the 'Environment Variables' button.
    In the 'System variables' section, find the Path variable and select it. Click 'Edit'.
    Add the directory where your krispy.bat file is located to the list of paths.\

5. Run `krispy` in your command prompt.
Easy enough.

