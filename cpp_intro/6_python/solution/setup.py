from setuptools import setup, Extension
from Cython.Build import cythonize
import os

ext_modules = [
    Extension(
        'fib_wrapper',
        sources=['fib_wrapper.pyx'],
        libraries=['fibonacci'],
        runtime_library_dirs=[os.path.abspath('build')],
        include_dirs=['include'],
        library_dirs=['build'],
    )
]


setup(
    name='fib_wrapper',
    version='0.0.1',
    ext_modules=cythonize(ext_modules)
)
