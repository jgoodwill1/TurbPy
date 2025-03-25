from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

extensions = [
    Extension("spectrum", ["src/spectrum.pyx"], include_dirs=[numpy.get_include()],
        extra_compile_args=["-O2"]),
]

setup(
    name="TurbPy",
    ext_modules=cythonize(extensions, language_level="3"),
    zip_safe=False,
)
