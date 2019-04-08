:point_right: Write some Python code that runs out of memory, i.e. causes a `MemoryError`.

:bulb: Here's one way to do it, using `numpy`:

```
$ python
>>> import numpy as np
>>> data = np.zeros(int(1e15), dtype='int8')
python(14642,0x7fff9847c380) malloc: *** mach_vm_map(size=1000000000000000) failed (error code=3)
*** error: can't allocate region
*** set a breakpoint in malloc_error_break to debug
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
MemoryError
```

I see some curious behaviour of `np.zeros` and `np.ones` that I don't understand yet.

`np.zeros` doesn't actually seem to allocate and fill the memory. I can make an array with size 1 TB.
```python
>>> data = np.zeros(int(1e12), dtype='int8')
>>> data.nbytes
1000000000000
```

`np.ones` does seem to allocate and fill the memory.
```python
>>> data = np.ones(int(1e12), dtype='int8')
```
In my system monitor I can see that this process is very slow (why?).
The process doesn't respond to `CTRL + C`, wo I have to kill it from the outside (using e.g. my system monitor).
