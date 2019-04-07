# Profiling Python code

This is a tutorial how to get started with profiling Python code by Christoph Deil.

We will only cover timing and profiling CPU and memory use.
Other kinds of profiling, or how to optimise will not be covered.

Throughout the tutorial you will find short exercises marked with :point_right:. Usually the solution is given directly below. Please execute the examples and try things for yourself. Interrupt with questions at any time!

This is the first time I'm giving a tutorial on this topic. Please let me know if you have any suggestions to improve!

## Outline

- [Prerequisites](#prerequisites)
- [1. When to profile?](#1-when-to-profile)
- [2. How to profile?](#2-how-to-profile)
- [3. What to profile?](#3-what-to-profile)
- [4. Measure CPU and memory usage](#4-measure-cpu-and-memory-usage)
- [5. Time code execution](#5-time-code-execution)
- [6. Function-level profiling](#6-function-level-profiling)
- [7. Line-level profiling](#7-line-level-profiling)
- [8. Memory profiling](#8-memory-profiling)
- [Things to remember](#things-to-remember)
- [Going further](#going-further)

## Questions

Please help me adjust the tutorial content and speed a bit:

- How often do you profile Python code? (never, last year, all the time)?
- Have you used `psutil` or `psrecord`?
- Have you used `time` or `%timeit`?
- Have you used `cProfile` or `%prun`?
- Have you used `line_profiler` or `%lprun`?
- Have you used `memory_profiler` or `%memit` or `%mprun`?
- Have you used any other Python profiling tool?

## Prerequisites

This tutorial assumes that you have used a terminal, Python, ipython and Jupyter before.
No experience with Python profiling is assumed, this tutorial will get you started and focus on the basics.

---

Before we start, let's make sure we have everything set up.

:point_right: Check your setup!

You should have `python` (Python 3.5 or later), `ipython`, `jupyter`, `psutil`, `psrecord`, `line_profiler`, `memory_profiler` and `snakeviz`. Use these commands to check:
```
python --version
ipython --version
jupyter --version
python -c 'import psutil, psrecord, line_profiler, memory_profiler, snakeviz'
```

:bulb: If something is missing, you can install it with pip:
```
python -m pip install psutil psrecord line_profiler memory_profiler snakeviz
```

## 1. When to profile?

You've probably heard this before: "Premature optimization is the root of all evil".

Timing and profiling is very much related to optimisation: you only do it if your code is too slow or you run out of memory.

The general recommendation concerning profiling and optimisation:

- Start by writing simple, clean, well-structured code.
- Establish correctness via automated test cases.
- Start using your code for your application.
- Never profile or optimise!

Computers these days are fast and have a lot of memory. Your time is precious. For the vast majority of code you write, optimisation and profiling are simply not needed.

Python and the libraries are so high-level, that you can write very advanced applications quickly. It's OK and advisable to re-factor or completly re-write using lessons learned from a first implementation, using better data structures, algorithms, or e.g. using [numba](https://numba.pydata.org/) for the small performance-critical part.

Of course, today is one of the few days in your life where you need to do profiling (you joined this tutorial), so let's do it.

## 2. How to profile?

Then the general recommendation is to proceed systematically in these steps:

- Write a "benchmark", a script that reflects a real use case where you want better performance.
- Define the key performance numbers (often runtime or peak memory usage) that you care about.
- Measure and write down current performance.
  Make sure your current code version is checked in to version control before starting the profiling and optimisation.
- Time and profile to find the performance bottlenecks
- Optimise only the parts where it matters.

The advice "measure first, using a real use case of your application" always holds. Python is a very dynamic language, understanding even basic performance characteristics is hard and surprising. E.g. attribute access and function calls are fast in most languages, but in Python are slow. For real complex applications it's impossible just from looking at the code.

## 3. What to profile?

In this section we will look a bit at the following components of your computer using Python examples:
- CPU (usually multi-core)
- memory
- disk
- network

In this tutorial we will mainly focus on CPU and memory. We will not cover I/O (disk and network) much, and not mention GPU or multi-CPU at all.

Note that your computer hardware and software is incredibly complex. It is quite common performance bottlenecks and behaviour is surprising and confusing. Also, results will differ, mostly based on your hardware and operating system.

---

To see what your system is doing, the easiest way is to use your system monitor tool. I'm on Mac, where it's an app called
[Activity Monitor](https://en.wikipedia.org/wiki/List_of_macOS_components#Activity_Monitor).

:point_right: Open up your system monitor tool.

:bulb: This tool is different for every operating system, so please use Google to find out how to do this.

---

Let's use [spam.py](spam.py) as an example of a Python script that uses up a lot of CPU and memory.

:point_right: Run `python spam.py` and observe the process with your system monitor.

# 4. Measure CPU and memory usage

Running the Python script starts a **process** and within the process runs your code in a single **thread**.

So only one CPU core will be used by your Python script, unless you call into Python C extensions that can use multiple CPU cores.

We will not need this for the rest of this tutorial, but sometimes it can be useful to know how to figure out the ID of your Python process or thread.

To find out the number of a Python process:
```python
>>> import os
>>> os.getpid()
```

To find out the active thread count, and thread identifier of the current thread:
```python
>>> import threading
>>> threading.active_count()
>>> threading.get_ident()
```

To learn more about threads and processes, and how to create and control them from Python, see the Python standard library [threading](https://pymotw.com/3/threading/), [multiprocessing](https://pymotw.com/3/multiprocessing/) and [subprocess](https://pymotw.com/3/subprocess/) modules. The [os](https://pymotw.com/3/os/) and [resource](https://pymotw.com/3/resource/) modules give you access to information about your operating system and sytem resources.

:point_right: Check how many CPU cores you have.
```python
>>> import multiprocessing
>>> multiprocessing.cpu_count()
```

Note that sometimes the number reported does not reflect the number of hardware CPU cores. E.g. I have an Intel CPU with 4 cores, but here and in the activity monitor see 8. This is due to [hyper-threading](https://en.wikipedia.org/wiki/Hyper-threading), where each physical CPU core appears as two logical cores.

---

In the Python standard library, things are pretty scattered and sometimes a bit cumbersome to use. Thankfully, there is a third-party Python package for process and system monitoring: [psutil](http://psutil.readthedocs.io/). To quote from the docs:

> psutil (python system and process utilities) is a cross-platform library for retrieving information on running processes and system utilization (CPU, memory, disks, network, sensors) in Python. It is useful mainly for system monitoring, profiling, limiting process resources and the management of running processes.

Let's try out just a few of the things `psutil` can do:
```python
import psutil
```

:point_right: How many CPU cores do you have? What frequency is your CPU?
```python
psutil.cpu_count()
psutil.cpu_count(logical=False)
psutil.cpu_freq() # In MHz
```

:point_right: How much memory do you have? How much free?
```python
psutil.virtual_memory().total / 1e9 # In GB
psutil.virtual_memory().free / 1e9 # In GB
```

:point_right: How much disk space do you have? How much free?
```python
psutil.disk_usage('/').total / 1e9
psutil.disk_usage('/').free / 1e9
```

:point_right: How many processes are running?
```python
len(psutil.pids())
```

The [recipes](http://psutil.readthedocs.io/en/latest/#recipes) section in the `psutil` docs contains examples how to find and filter and control processes.

---

To get information about a specific process, you create a `psutil.Process` object. By default, the process will be the current process (with the number given by `os.getpid()`)
```python
>>> psutil.Process()
psutil.Process(pid=19651, name='python3.6', started='18:01:23')
```
But you can create a `psutil.Process` object for any process running on your machine, by giving the `PID`.

:point_right: Print the `pid` and `name` of the last 10 processes started.
```python
for pid in psutil.pids()[:10]:
    p = psutil.Process(pid)
    print(p.pid, p.name())
```

:point_right: Print the current CPU and memory use of the current process.
```python
p = Process()
p.cpu_percent()
p.memory_full_info().rss / 1e6 # in MB
```

Note that the CPU percent is given per core. So if you have 4 cores and a process that uses all of them, it will show up with `cpu_percent = 400`. To quote from the docs [here](http://psutil.readthedocs.io/en/latest/#psutil.Process.cpu_percent):


> The returned value is explicitly NOT split evenly between
all available logical CPUs. This means that a busy loop process
running on a system with 2 logical CPUs will be reported as
having 100% CPU utilization instead of 50%.


The `psutil` docs are very good; one gotcha to watch out for is that some functions appear twice, e.g. there is [psutil.cpu_percent](http://psutil.readthedocs.io/en/latest/#psutil.cpu_percent) for the whole system, and there is [psutil.Process.cpu_percent](http://psutil.readthedocs.io/en/latest/#psutil.Process.cpu_percent) for a given process.

---

You can use `psutil` directly from your script, or use tools built on top of `psutil`. There are some [example applications](https://github.com/giampaolo/psutil#example-applications), many [projects using psutil](https://github.com/giampaolo/psutil#projects-using-psutil) and [ports](https://github.com/giampaolo/psutil#portings) to other languages.

One tool I find nice is [psrecord](https://github.com/astrofrog/psrecord), which makes it simple to record and plot the CPU and memory activity of a given process.

:point_right: Run [compute_and_io.py](compute_and_io.py) through `psrecord`.
```
psrecord --help
psrecord --interval 0.1 --plot compute_and_io.png --log compute_and_io.txt 'python compute_and_io.py'
head compute_and_io.txt
open compute_and_io.png
```

For me, this takes about 7 seconds:
```
$ psrecord --interval 0.1 --plot compute_and_io.png --log compute_and_io.txt 'python compute_and_io.py'
Starting up command 'python compute_and_io.py' and attaching to process
0.000 sec :  starting computation
0.352 sec :  starting network download
2.753 sec :  starting more computation
5.873 sec :  starting disk I/O
6.673 sec :  done
Process finished (7.09 seconds)
```

In the recorded [compute_and_io.png](compute_and_io.png) one can nicely see the typical behaviour of Python processes:
- One thread runs on one core at 100% CPU utilisation while you're doing computations. The Python interpreter is basically a `while True: execute next byte code` loop.
- And when disk or network I/O happens, Python makes calls into the operating sytem, and the CPU utilisation is lower. It can be between 0% and 100%, depending on the I/O task and your computer.

Note that Numpy, Scipy, Pandas or other libraries you use might use multiple CPU cores in some functions (see [here](https://scipy.github.io/old-wiki/pages/ParallelProgramming)
). E.g. to compute the doc product of two arrays, [numpy.dot](https://docs.scipy.org/doc/numpy/reference/generated/numpy.dot.html) calls into a linear algebra library  and often uses multiple CPU cores if they are available and if that would speed up the computation. Sometimes more cores don't help because the bottleneck is the data access from memory. The performance of a given script might be very different not just depending on your CPU, but also your software (e.g. Numpy and BLAS), see e.g. [here](http://markus-beuckelmann.de/blog/boosting-numpy-blas.html). Anaconda by default gives you a high performance [Intel MKL](https://en.wikipedia.org/wiki/Math_Kernel_Library).

:point_right: Use `numpy.show_config` to see which linear algebra library (called BLAS and LAPACK) you are using.

:point_right: Run `psrecord` on [multi_core.py](multi_core.py).

```
psrecord --interval 0.1 --plot multi_core.png 'python multi_core.py'
```
On my machine, [numpy.random.random_sample](https://docs.scipy.org/doc/numpy/reference/generated/numpy.random.random_sample.html) uses one core, and [numpy.dot](https://docs.scipy.org/doc/numpy/reference/generated/numpy.dot.html) uses all four available cores: [multi_core.png](multi_core.png).

If you want to write functions yourself that use multiple cores, this is possible with Numba, Cython or from any C extension, but not from normal Python code. If you're interested in this, see e.g. [here](https://python-notes.curiousefficiency.org/en/latest/python3/multicore_python.html) or [here](https://devblogs.nvidia.com/seven-things-numba/).

---

`psutil` can also help you with disk or network I/O and monitoring or controlling subprocesses. We won't go into this here, just one quick example:

:point_right: Get a list of open files for your process.
```python
import psutil
p = psutil.Process()
p.open_files()
fh = open('spam.py')
p.open_files()
fh.close()
p.open_files()
```

## 5. Time code execution

Total runtime of your analysis is often the most important performance number you care about.

To time the execution of a Python script, you can use the [Unix time command](https://en.wikipedia.org/wiki/Time_(Unix)).

:point_right: Time the `python` interpreter startup. Time  `import numpy`.

```
$ time python -c ''
real	0m0.038s
user	0m0.025s
sys	0m0.008s

$ time python -c 'import numpy'

real	0m0.141s
user	0m0.105s
sys	0m0.032s
```
Detailed information about the three times is given
[here](https://stackoverflow.com/questions/556405/) and
[here](https://www.quora.com/Unix-What-is-the-difference-between-real-user-and-sys-when-I-call-time). Basically:

- The `real` time is the wall clock time. It's what you usually care about and want to be small.
- The `user` and `sys` are the time spent in "user mode" and "in the kernel". You usually don't care about this.

Note that `real` time, i.e. wall clock time, doesn't depend on the number of CPU cores that was used. But `user` and `sys` does, for processes that use multiple cores, they can be larger than the `real` time. Here's an example:
```
$ time python multi_core.py
a
b
c

real	0m15.656s
user	0m51.727s
sys	0m0.895s
```

If you want to time only part of your Python script, you can use the Python standard library [time](https://pymotw.com/3/time/index.html) module, specifically the `time.time` function, like this:
```python
import time
t_start = time.time()
# start of code you want to time
time.sleep(2)
# end of code you want to time
t_run = time.time() - t_start
print('t_run:', t_run)
```
We already saw this above in the example using [compute_and_io.py](compute_and_io.py).

If you want to do more precise timing of small bits of Python code (say less that 1 second) use [timeit](https://pymotw.com/3/timeit/).

Both [%time](http://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-time) and [%timeit](http://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-timeit) are available from ipython and Jupyter.

We've already used this a lot yesterday, so let's move on.

## 6. Function-level profiling

The examples above using `psutil` and `psrecord` use "sampling" at regular time intervals "from the outside" to measure the CPU and memory usage. This can be useful to see the overall performance of your process, but the connection to your Python code is lost, to understand and optimise you need something different.

The Python standard library contains a deterministic function-level profiler. It traces the execution of your Python code, and records every function call and return (a more detailed explanation is [here](https://docs.python.org/3.6/library/profile.html#what-is-deterministic-profiling)). Then at the end, you can examine the stats to find which functions were run how often and how much time is spent in each function.

Note: :astonished: The Python standard library has a `profile` and `cProfile` that do the same thing. :confused: Only `profile` is implemented in Python and slower and `cProfile` in C and faster. So you should always use `cProfile`. :relieved:

:point_right: Run the [compute.py](compute.py) script through the Python profiler.
```
$ python -m cProfile --help
Usage: cProfile.py [-o output_file_path] [-s sort] scriptfile [arg] ...

Options:
  -h, --help            show this help message and exit
  -o OUTFILE, --outfile=OUTFILE
                        Save stats to <outfile>
  -s SORT, --sort=SORT  Sort order when printing to stdout, based on
                        pstats.Stats class

$ python -m cProfile compute.py
         30 function calls in 0.114 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.002    0.002    0.114    0.114 compute.py:1(<module>)
        2    0.000    0.000    0.088    0.044 compute.py:1(generate_data)
        1    0.001    0.001    0.113    0.113 compute.py:10(main)
        2    0.088    0.044    0.088    0.044 compute.py:2(<listcomp>)
        2    0.000    0.000    0.023    0.012 compute.py:4(compute_result)
        1    0.000    0.000    0.114    0.114 {built-in method builtins.exec}
       20    0.023    0.001    0.023    0.001 {built-in method builtins.sum}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
```

:point_right: Use `compute.py` through `cProfile` and store the resulting stats in `compute.stats`. Use `pstats` to read and view the stats in different ways.
```
$ python -m cProfile -o compute.prof compute.py
$ python -m pstats
Welcome to the profile statistics browser.
% help

Documented commands (type help <topic>):
========================================
EOF  add  callees  callers  help  quit  read  reverse  sort  stats  strip

% read compute.prof
compute.prof% stats
Tue Jun  5 17:07:43 2018    compute.prof

         30 function calls in 0.109 seconds

   Random listing order was used

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.109    0.109 {built-in method builtins.exec}
       20    0.023    0.001    0.023    0.001 {built-in method builtins.sum}
        2    0.084    0.042    0.084    0.042 compute.py:2(<listcomp>)
        1    0.001    0.001    0.107    0.107 compute.py:10(main)
        1    0.002    0.002    0.109    0.109 compute.py:1(<module>)
        2    0.000    0.000    0.023    0.011 compute.py:4(compute_result)
        2    0.000    0.000    0.084    0.042 compute.py:1(generate_data)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}


compute.prof% sort ncalls
compute.prof% stats
Tue Jun  5 17:07:43 2018    compute.prof

         30 function calls in 0.109 seconds

   Ordered by: call count

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
       20    0.023    0.001    0.023    0.001 {built-in method builtins.sum}
        2    0.084    0.042    0.084    0.042 compute.py:2(<listcomp>)
        2    0.000    0.000    0.023    0.011 compute.py:4(compute_result)
        2    0.000    0.000    0.084    0.042 compute.py:1(generate_data)
        1    0.000    0.000    0.109    0.109 {built-in method builtins.exec}
        1    0.001    0.001    0.107    0.107 compute.py:10(main)
        1    0.002    0.002    0.109    0.109 compute.py:1(<module>)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}


compute.prof% quit
Goodbye.
```

The `cProfile` and `stats` are described in detail in the tutorials [here](https://pymotw.com/3/profile/index.html) or [here](https://docs.python.org/3.6/library/profile.html). They are very powerful, but can be a bit cumbersome to use. Let's look at two user-friendly options that use `cProfile` under the hood.

---

From `ipython` or `jupyter` you can use the `%prun` or `%%prun` magic commands (see [docs](http://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-prun) or bring up the help via `%prun?`).

:point_right: Import `compute` and `%prun` the `compute.main()` function.
```
$ ipython

In [1]: %prun?

In [2]: import compute

In [3]: %prun compute.main()
         30 function calls in 0.114 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        2    0.086    0.043    0.086    0.043 compute.py:2(<listcomp>)
       20    0.025    0.001    0.025    0.001 {built-in method builtins.sum}
        1    0.002    0.002    0.114    0.114 <string>:1(<module>)
        1    0.001    0.001    0.112    0.112 compute.py:10(main)
        2    0.000    0.000    0.025    0.013 compute.py:4(compute_result)
        1    0.000    0.000    0.114    0.114 {built-in method builtins.exec}
        2    0.000    0.000    0.086    0.043 compute.py:1(generate_data)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
```
---

The functionality from `pstats` is OK to understand the profile results. But often being able to quickly visualise and browse the results is nicer. For this, you can use [snakeviz](https://jiffyclub.github.io/snakeviz/).

:point_right: Open `compute.prof` with `snakeviz`.
```
$ snakeviz compute.prof 
snakeviz web server started on 127.0.0.1:8080; enter Ctrl-C to exit
```
Make sure you explore the output a bit, especially try both "Sunburst" and "Icicle" for the style.

:point_right: Do you prefer the stats table, or the sunburst, or the icicle?

## 7. Line-level profiling

With function-level profiling you can find the functions that are relevant to the performance of your application.
 But what if you want to know which lines of code in the function are slow? The [line_profiler](https://github.com/rkern/line_profiler) package let's you measure execution time line by line, from Python, ipython or Jupyter.

For this section, we will switch to the [Profiling and Timing Code](https://jakevdp.github.io/PythonDataScienceHandbook/01.07-timing-and-profiling.html) Jupyter notebook from the excellent [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/) by Jake VanderPlas. It's freely available at https://github.com/jakevdp/PythonDataScienceHandbook and generally is a great resource to learn, so I wanted to introduce it.

:point_right: Clone the `PythonDataScienceHandbook` git repository and start Jupyter.
```
cd <where you have your repositories>
git clone https://github.com/jakevdp/PythonDataScienceHandbook.git
cd PythonDataScienceHandbook
jupyter notebook notebooks/01.07-Timing-and-Profiling.ipynb
```

## 8. Memory profiling

You want your program to fit in main memory. If it doesn't, then the operating system will either start swapping to disk, which is slow, or kill your process.

In this section we look a bit how you can figure out how much memory your Python program uses, and how to figure out where that memory is allocated.

---

:point_right: Write some Python code that runs out of memory, i.e. causes a `MemoryError`.

:bulb: See [memory_error.md](memory_error.md)

This is surprisingly difficult, because depending on your operating system and configuration, it might start swapping to disk. So allocating more memory than you have RAM might work just fine. [psutil.swap_memory](http://psutil.readthedocs.io/en/latest/#psutil.swap_memory) can give some info on this.

---

:point_right: To find the peak memory use of a program, you can run it through `psrecord` and then take the max of the third column "Real (MB)"

```python
import pandas as pd
df = pd.read_csv(
      'compute_and_io.txt',
      skiprows=1, delim_whitespace=True,
      names=['t', 'cpu', 'mem', 'vmem'],
)
mem_max = df['mem'].max()
print(f'Max memory: {mem_max} MB')
```

---

Now what if you're using too much memory, and would like to know why?

First of all, it helps to know a bit about how Python stores data. As explained [here](https://jakevdp.github.io/PythonDataScienceHandbook/02.01-understanding-data-types.html), a python `int` of `float` is more than just an `int` or `float` in C. Similarly, e.g. a `list` uses more memory than an array in C.

:point_right: Use [sys.getsizeof](https://docs.python.org/3/library/sys.html#sys.getsizeof) to measure the size (in bytes) of a few objects:
```python
>>> import sys
>>> sys.getsizeof(42) # int
28
>>> sys.getsizeof('spam') # str
53
>>> sys.getsizeof({}) # empty dict
240
>>> sys.getsizeof([]) # empty list
64
>>> sys.getsizeof([42]) # list with one int
72
>>> import numpy as np
>>> data = np.ones(1000) # default dtype is float with 64 bit = 8 byte
>>> sys.getsizeof(data)
8096
```

Some Python objects have convenience methods to get their memory use. Especially there is [numpy.ndarray.nbytes](https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.nbytes.html):
```python
>>> import numpy as np
>>> array = np.ones(1000)
>>> array.nbytes
8000
>>> array.size
1000
>>> array.itemsize
8
```
Pandas shows the memory used by a data frame via [data_frame.info](data_frame.info)
```python
>>> import pandas as pd
>>> df = pd.DataFrame({'a': [1, 2], 'b': [3.3, 4.4]})
>>> df.info()
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 2 entries, 0 to 1
Data columns (total 2 columns):
a    2 non-null int64
b    2 non-null float64
dtypes: float64(1), int64(1)
memory usage: 112.0 bytes
```

---

There is also the [memory_profiler](https://github.com/pythonprofilers/memory_profiler) which you can use to monitor memory usage or even look at line by line increment / decrement of memory usage.

:point_right: Let's use the [01.07-Timing-and-Profiling.ipynb](https://jakevdp.github.io/PythonDataScienceHandbook/01.07-timing-and-profiling.html#Profiling-Memory-Use:-%memit-and-%mprun) to try this out. (See last section how to get it.)

## Things to remember

### General

- Profiling is hard. Performance depends on your code, data and parameters, but also on your CPU, C compiler, Python, libraries, ...
- Only profile and optimise if needed. Most of the time you don't.
- Always measure and profile a real use case before starting to optimise. Often the measure of interest is runtime, sometimes memory use or disk I/O or other things.
- Usually data structures and algorithms are more important than micro optmisations.

### Tools

- Python provides great tools for timing and profiling code.
- Use `psutil` and `psrecord` to measure and record CPU and memory use. You can use this on any process, not just Python.
- Use the Unix `time`, Python standard library `time` or `timeit`, and ipython / Jupyter `%time`, `%timeit` line and `%%time`, `%%timeit` cell magic commands to measure CPU time.
- To profile CPU usage, the Python standard library provides  `cProfile` and `pstats`. The `%prun` and `snakeviz` make this nice to use. This is a "deterministic function-level profiler", i.e. works by tracing function calls.
- Use `line_profiler` and included `kernprof`, `%lprun`, `%%lprun` to line-by-line profiling for a given function. Again, this is a deterministic profiler tracing line execution.
- There are also "sampling profilers" that sample a process at given time intervals. This is what `psrecord` does, and also what system monitor tools do. We didn't cover them here, but some links to other profilers are given in the next section.
- Use `memory_profiler` to monitor the memory usage of Python code. `%memit` for a single statement, and `%mprun` for line-by-line profiling of a given function.
- Use `sys.getsize` or Numpy `array.nbytes` or Pandas `data_frame.info()` to see the memory usage for a given object.

## Going further

If you'd like to learn more, here's how you can go further:

- If you only read through this tutorial, go back to the start and type and execute the exercises to make it stick. They are marked with :point_right:.
- We did not do a real-word complex example here. Take some of your application code or data analysis and time and profile it to practice. Is it I/O or CPU limited? How much peak memory does it use? Which functions or lines are the bottleneck?
- The [Profiling and Timing Code](https://jakevdp.github.io/PythonDataScienceHandbook/01.07-timing-and-profiling.html) notebook from the [Python data science handbook](https://jakevdp.github.io/PythonDataScienceHandbook/) by Jake VanderPlas covers similar material, executing everything from the Jupyter notebook.
- The [How to optimize for speed](http://scikit-learn.org/dev/developers/performance.html) page in [scikit-learn](http://scikit-learn.org/) docs, which contains a bit of infos on profiling C extensions as well.
- The [profile and pstats — Performance Analysis](https://pymotw.com/3/profile/) tutorial from the [Python module of the week](https://pymotw.com/) by Doug Hellman is a very detailed overview of `cProfile` and `pstats`.
- The [README](https://github.com/giampaolo/psutil/blob/master/README.rst) and [docs](http://psutil.readthedocs.io/) of `psutil` give a good overview of all the things you can monitor and measure about your sytem and process.
- The [snakeviz](http://jiffyclub.github.io/snakeviz/) docs contain descriptions and examples of how to visually explore the profile stats.
- The [line_profiler](https://github.com/rkern/line_profiler/blob/master/README.rst) docs.
- the [memory_profiler](https://github.com/pythonprofilers/memory_profiler/blob/master/README.rst) docs.

There are other Python profiling and visualisation tools. I didn't try them yet, but

- [PyCharm](https://www.jetbrains.com/pycharm/) has a [profiler](https://www.jetbrains.com/help/pycharm/profiler.html), but only in the non-free professional edition.
- [vmprof-python](https://github.com/vmprof/vmprof-python) - a statistical program profiler
- [yappi](https://bitbucket.org/sumerc/yappi/) - Yet Another Python Profiler
- [vprof](https://github.com/nvdv/vprof) - Visual profiler for Python
- [plop](https://github.com/bdarnell/plop) - Python Low-Overhead Profiler
- [pyinstrument](https://github.com/joerick/pyinstrument) - Call stack profiler for Python. Shows you why your code is slow!
- [gprof2dot](https://github.com/jrfonseca/gprof2dot) - Converts profiling output to a dot graph
- [pyprof2calltree](https://github.com/pwaller/pyprof2calltree/) - Profile python programs and view them with kcachegrind
- [PyFlame](https://eng.uber.com/pyflame/) - A Ptracing Profiler For Python
- Intel [VTune](https://en.wikipedia.org/wiki/VTune) - Supports many languages, including Python

We did not have time to cover **optimisation**.

If you'd like to make your code faster, here's some things you could look at:

- Get to know the data structures and the performance characteristics of Python types (numbers, lists, dicts, objects) as well as `numpy` and `pandas`. The slides from David Beazley [here](http://www.dabeaz.com/datadeepdive/) give a good overview.
- Vectorise your code using `numpy`.
- If your algorithm isn't easy to express in vectorised form with `numpy`, or if `numpy` is too slow or uses too much memory, try [Numba](http://numba.pydata.org/) or [Cython](http://cython.org/). There are a lot of tutorials and comparisons available online. A recent one that contains a good summary and link collection at the top is [The case for Numba](http://matthewrocklin.com/blog/work/2018/01/30/the-case-for-numba) by Matthew Rocklin.
- To take advantage of multiple cores, try [multiprocessing](https://pymotw.com/3/multiprocessing) from the Python standard library. Also look at [Dask](https://dask.pydata.org/).
- If you're willing to consider other languages to write a Python C extension, you have options which language to use:
  - You can write in Cython and it will generate C.
  - If you use C, popular options to interface include `CFFI` and `Cython` (as well as others, see e.g. [here](http://docs.python-guide.org/en/latest/scenarios/clibs/))
  - For C++, traditionally SWIG and Cython and Boost.Python have been frequently, but recently I think [pybind11](https://github.com/pybind/pybind11) has become the tool of choice.
  - [Julia](https://julialang.org/) has very good interfacing to [PyCall](https://github.com/JuliaPy/PyCall.jl). From what I've seen, it's not commonly used though to ship with Python libraries, probably because it's new and harder to support installation for the many different machines and distributions users have. For other modern languages like [rust](https://www.rust-lang.org/) or [go](https://golang.org/) it's similar as far as I know.