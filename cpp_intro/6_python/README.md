# Interface our cpp shared library from python using cython

Were are writing a small python module using Cython,
to call the fib function from python.

Note: We are not calling cmake from the setup.py file,
this means, this package is not simply pip installable.
This will be left as an exercise to the reader ;-)
(An example setup.py which calls cmake is at
https://github.com/pybind/cmake_example/blob/master/setup.py)

So for now, in the end it should be:
```
mkdir build
cd build
cmake ..
make
cd ..
pip install -e .
```

## References

* https://cython.org/
* https://setuptools.readthedocs.io/en/latest/setuptools.html
