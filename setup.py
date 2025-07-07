from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

extensions = [
    Extension(
        name="turbPy.spectrum",
        sources=["turbPy/spectrum.pyx"],
        include_dirs=[numpy.get_include()],
        extra_compile_args=["-std=c99"],
    )
]

setup(
    name="turbpy",
    packages=["turbPy"],
    ext_modules=cythonize(extensions),
)
