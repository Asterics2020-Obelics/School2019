from setuptools import setup, Extension
from Cython.Build import cythonize

ext_modules = [
    Extension(
        'fib_wrapper',
        sources=['fib_wrapper.pyx'],
        libraries=['fibonacci'],
        runtime_library_dirs=['build'],
        include_dirs=['include'],
        library_dirs=['build'],
    )
]


setup(
    name='fib_wrapper',
    ext_modules=cythonize(ext_modules)
)
