# Debugging Python code

This is a tutorial how to get started with debugging Python code by Christoph Deil.

We will start by looking at how Python executes code, exceptions and stack frames first, and only in the second half move on to using a debugger.

Throughout the tutorial you will find short exercises marked with :point_right:. Usually the solution is given directly below. Please execute the examples and try things for yourself. Interrupt with questions at any time!

This is the first time I'm giving a tutorial on this topic. Please let me know if you have any suggestions to improve!

## Outline

- [Prerequisites](#prerequisites)
- [1. When to debug?](#1-when-to-debug)
- [2. How Python executes code](#2-how-python-executes-code)
- [3. Exceptions and tracebacks](#3-exceptions-and-tracebacks)
- [4. Debugging with pdb](#4-debugging-with-pdb)
- [5. Debugging with ipython and Jupyter](#5-debugging-with-ipython-and-jupyter)
- [6. Debugging with PyCharm](#6-debugging-with-pycharm)
- [Things to remember](#things-to-remember)
- [Going further](#going-further)

## Questions

Please help me adjust the tutorial content and speed a bit:

- How often do you debug Python code? (never, last year, all the time)?
- Do you know how Python executes code?
- Do you know what exceptions and stack frames are and how to read a traceback?
- Have you used `pdb` to debug from Python?
- Have you used `%debug` or `%run -d` from ipython or Jupyter?
- Have you used the `PyCharm` debugger?
- Have you used any other Python debugging tool?

## Prerequisites

This tutorial assumes that you have used a terminal, Python, ipython and Jupyter before. No experience with Python debugging is assumed, this tutorial will get you started and focus on the basics.


:point_right: Check that you have Python (3.5 or later), `ipython` and `jupyter` installed

```
$ python --version
$ ipython --version
$ jupyter --version
```

If you don't have this, one nice option to get it is [Anaconda Python](https://www.anaconda.com/download/).

At the end of this tutorial, i will demo how to use the visual debugger in PyCharm.

If you want to try it out, install the free community edition
of [PyCharm](https://www.jetbrains.com/pycharm/download/).
After installing PyCharm, you need to configure two things:
your Python interpreter and execute `Tools | Create Command-line Launcher`.

:point_right: Check that you have PyCharm installed and configured.

One way to launch PyCharm is to cd into the directory for this tutorial
and use the command line launcher like this:
```
cd python-tutorials/debug
charm .
```
Then right-click on `analysis.py` and select "run analysis".
A console at the bottom should appear the output of "5.0" that we print from that script.

*Note: there are many other editors and IDEs that have Python debugging support
(either built in or via extensions), e.g. `vim` or `emacs` or [Visual Studio
Code](https://code.visualstudio.com/). I'm not familiar with those, and in any
case we will not have time to sort out installation / setup problems for those
during the tutorial. If you want to use those, try them after the tutorial and
try to re-do the examples from this tutorial.*

## 1. When to debug?

### Suspect result

When you have an incorrect or at least suspect output of your program, you have to investigate your code and data to try and pin down why the output is not what you expect. This is the worst, compared to this issue, the next two cases are nice, because it's obvious that there's a problem and you get a traceback with lots of info where to start looking.

### Exception

Most of the time you will be able to read the traceback and code and figure out what is wrong and not need to start a debugger. But sometimes it's not clear and you need to 'look around'; that's when you start a debugger.

### Crash

The Python process can crash. This is very rare, except if you work on or use buggy Python C extensions. To debug it you would use `gdb` or `lldb`. There are tutorials (see e.g. [here](http://www.scipy-lectures.org/advanced/debugging/index.html#debugging-segmentation-faults-using-gdb)), we won't cover it here.

:point_right: Cause Python to crash.

```
$ python
>>> import ctypes
>>> ctypes.string_at(1)
Segmentation fault: 11
$
```


## 2. How Python executes code

To debug Python code, you need to know how Python executes code.
Have a look at the Python module [point.py](point.py) that defines
a `Point` class and a `distance` function, and the [analysis.py](analysis.py)
script that does `from point import Point, distance` and runs a simple analysis.

Is it clear what happens when you run `python analysis.py`?

The short answer is that Python executes code top to bottom, line by line. When
a `def` or `class` statement is encountered, a function or `type` object are
created in the module `namespace`, and `import point` causes the code in
`point.py` to be executed, and when the bottom is reached, the `point` module is
stored in the global `sys.modules` dict, i.e. a second `import point` will be a
no-op, not execute the code in `point.py` again. You should never reload in
Python, always restart the interpreter if you edit any code.

If you're not sure what Python does with `def` or `class` or `import`, please
ask now, and we'll spend a few minutes to add print statements to show what is
going on.

Another important concept you need to know about is how Python variables and
function calls work. Superficially Python seems similar to C or C++, there are
variables to store data and function calls create stack frames. But if you look
a bit closer, you'll see that it works completely differently under the hood: in
Python everything is an object, variables are entries in namespace dictionaries
(`globals()` and `locals()`) pointing to objects, and Python is dynamic, i.e.
happy to have an integer variable `data = 999` and then on the next line change
to a string variable `data = 'spam'`. Memory management is automatic, using a
reference counting garbage collector that deletes objects with zero references.
Python is both "compiled" and "interpreted": code is parsed into an `ast`
(abstract syntax tree), compiled into `bytecode`, and executed by the `CPython`
"interpreter" or "virtual machine", which executes one byte code after the other
in an infinite `while` loop.

Most Python programmers don't know how Python works "under the hood". That's good, Python is supposed to be a high-level language that "fits your brain" and does what you intuitively expect. But you still need to have a "mental model" about variables, objects and the stack of function calls, each with it's own local namespace. The best way to learn about this is actually to step through code and see how the Python program state changes. Before we do this in a debugger, check this out:

:point_right: Step through the [point example](https://goo.gl/yTEbLX) using http://pythontutor.com/.

If you'd like to learn more, the [Whirlwind Tour Of
Python](http://nbviewer.jupyter.org/github/jakevdp/WhirlwindTourOfPython/blob/master/Index.ipynb)
is a beginner-level introduction, and [Python
epiphanies](https://nbviewer.jupyter.org/github/oreillymedia/python_epiphanies/blob/master/Python-Epiphanies-All.ipynb)
is a notebook explaining everything in great detail.

## 3. Exceptions and Tracebacks

If you use Python, you will see exceptions and tracebacks all the time.

In Python, the term "error" is often used to mean the same thing as "exception".
Although of course, "error" and "exception" are very general terms and are
widely used, not always referring to a Python exception (i.e. instances of the
built-in `Exception` class or subclasses of `Exception` like `TypeError`).

Once you've learned to read a traceback, there will be many times where
it's enough information for you to figure out what's wrong,
and you will only start the debugger in the cases where the problem
isn't clear from reading the traceback and relevant code for a minute or two.

Example: [exception.py](exception.py)
```python
$ python exception.py
Traceback (most recent call last):
  File "exception.py", line 14, in <module>
    main()
  File "exception.py", line 12, in main
    move_it(p)
  File "exception.py", line 8, in move_it
    point.move(42, '43')
  File "/Users/deil/code/python-tutorials/debug/point.py", line 16, in move
    self.y += dy
TypeError: unsupported operand type(s) for +=: 'int' and 'str'
```

Sometimes you will see a "chained exception" (also called "double inception"),
where a second exception is raised inside an exception handler, i.e. an `except`
block.

Example: [chained_exception.py](chained_exception.py)
```
$ python exception_chain.py
Traceback (most recent call last):
  File "exception_chain.py", line 4, in <module>
    a / b
ZeroDivisionError: division by zero

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "exception_chain.py", line 6, in <module>
    print('Bad data:', a, c)
NameError: name 'c' is not defined
```

:point_right: Start `python` and create some of the most common exceptions.

These are some very common errors you'll see a lot:
- `SyntaxError`
- `IndentationError`
- `NameError`
- `AttributeError`
- `KeyError`
- `IndexError`

:point_right: What other exceptions have you seen? Are they clear or do you have any question?

There's more info on Python exceptions [here](https://docs.python.org/3/tutorial/errors.html) and an overview of all built-in exceptions [here](https://docs.python.org/3/library/exceptions.html#exception-hierarchy).

## 4. Debugging with pdb

Let's use the Python scripts from above ([exception.py](exception.py) and [silent_error.py](silent_error.py)) to debug with `pdb`, the Python debugger.

- with print statements
- `import pdb; pdb.set_trace()`
- `python -m pdb myscript.py`

## 5. Debugging with ipython and Jupyter

Similarly how `ipython` and `jupyter` often give a nicer interactive Python environment than `python`, they also make it often easier to debug.

- `ipython -i`
- `import IPython; IPython.embed()`
- `ipdb`

To learn debugging from Jupyter, let's use the [Errors and Debugging](https://jakevdp.github.io/PythonDataScienceHandbook/01.06-errors-and-debugging.html) notebook from the the excellent [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/) by Jake VanderPlas. It's freely available at https://github.com/jakevdp/PythonDataScienceHandbook and generally is a great resource to learn, so I wanted to introduce it.

:point_right: Clone the `PythonDataScienceHandbook` git repository and start Jupyter.
```
cd <where you have your repositories>
git clone https://github.com/jakevdp/PythonDataScienceHandbook.git
cd PythonDataScienceHandbook
jupyter notebook notebooks/01.07-Timing-and-Profiling.ipynb
```

- `%debug`
- `%run -d`
- `%pdb`

## 6. Debugging with PyCharm

PyCharm has a great visual debugger. 

Since PyCharm is visual, it's hard to write a tutorial so that you can follow
along offline by just reading the info here.
Note that the PyCharm folks have a tutorial on debugging with many
screenshots [here](https://www.jetbrains.com/help/pycharm/debugging-code.html)
and a 6 min video on Youtube [here](https://www.youtube.com/watch?v=QJtWxm12Eo0).

One way to launch PyCharm is to cd into the directory for this tutorial
and use the command line launcher like this:
```
cd python-tutorials/debug
charm .
```

:point_right: Right-click on `analysis.py` and select "debug analysis".

## Things to remember

- Python is a very dynamic language
  - Very powerful
  - Easy to make mistakes
  - Easy to inspect and debug
- Use `pdb` from Python and `ipdb` from ipython and Jupyter for debugging, or a visual debugger like e.g. the one from Pycharm.
- See the debugger commands with `help` or [here](https://docs.python.org/3.6/library/pdb.html#debugger-commands).
- From ipython / jupyter, the commands are `%debug`, `%run -d` and `%pdb`
- Most people don't use a debugger often. There's code reading and `print` and `IPython.embed()` or just using ipython and the Jupyter notebook to see what's going on.

## Going further

These are good resources to learn more:

- Use http://pythontutor.com/ to learn how Python executes code.
- The [Errors and Debugging](https://jakevdp.github.io/PythonDataScienceHandbook/01.06-errors-and-debugging.html) page from the [Python data science handbook](https://jakevdp.github.io/PythonDataScienceHandbook/) by Jake VanderPlas.
- The Python standard library documentation for `pdb` ([link](https://docs.python.org/3.6/library/pdb.html))
- The Python module of the week tutorial for `pdb` by Doug Hellman ([link](https://pymotw.com/3/pdb/index.html))
- The [Python Debugging With Pdb](https://realpython.com/python-debugging-pdb/) tutorial by Nathan Jennings.
- The [Machete mode debugging](https://nedbatchelder.com/text/machete.html) talk by Ned Batchelder is fun and educational.
- [Software debugging](https://eu.udacity.com/course/software-debugging--cs259) free course on Udacity by Andreas Zeller. (I only watched the 1 min intro, don't know if it's any good.)
