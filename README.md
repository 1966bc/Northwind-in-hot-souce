# Northwind-in-hot-souce

Tkinter vs wxPython comparison

[![Python 3](https://img.shields.io/badge/python-3%20-blue.svg)](https://www.python.org/downloads/)
[![Tkinter](https://img.shields.io/badge/Tkinter%20-green.svg)](https://docs.python.org/3/library/tk.html)
[![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg)](https://www.sqlite.org/index.html)


![alt tag](https://user-images.githubusercontent.com/5463566/216831264-fc650f4c-b847-432c-a9d0-56d4feb2e79c.png)

Hello, this project has the ambition to demonstrate the use and 
thus the preformance of two of the most popular graphical toolkits
used in the Python environment, Tkinter and wxPython.
I basically wrote the same program using the two libraries,
trying to set the two versions with the same functionality.
The program allows you to view and perform the basic functionality
such as insert, edit and delete, on a database,
which on this occasion is a sqlite database, and specifically the 
Microsoft's famous Northwind database.

As far as wxPython is concerned, I used a very Pythonic approach,
for example I did not use the default IDs, preferring to call
the various widgets directly, instead of using their IDs which is what
is done in wxPython and which should be derived from the wx libraries and thus 
from the C++ with which they are written.

As for the version in Tkinter, this is nothing more than
the reincarnation of an old project of mine, "Tkinterlite," which you can find
on my github site, in which I show how to use Python, Tkinter and SQLite
together.

The project is still far from complete as there are
a number of things that I do better in Tkinter than in wxPython.
For example, the layout of the frame I can't handle 100%.
But also the event handling, I think I use it better in Tkinter
than in wxPython.
But maybe my main limitation is that I program in Tkinter and wxPython
equally, i.e., I do not adapt, out of ignorance of wxPython I think, 
to the features of the wxPython library, which, you can see from how the
called the methods and properties of the various classes, are affected by their
origin, even though I know C.

So if there is anyone who wants to propose changes, please know
that it is welcome.
Have fun with it.

P.S.
I have created two folders for the two versions.
To launch the ordnance you have to run the file called
northwind.py present in the respective folders, which means that if 
you are on Windows you can launch it using python idle directly,
or by running it from the command line, whereas if you are on linux, 
from where I write you can launch it from the shell making it executable 
after running something like this
chmod +x northwind.py
and then
./northwind
