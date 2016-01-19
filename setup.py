# distribution: python setup.py sdist --format=zip
# install: python setup.py build && python setup.py install

from distutils.core import setup, Extension
import glob
import SimpleQmap


hsmsources = glob.glob("SimpleQmap/source_files/libhsm/*.c")
hsm_module = Extension('libhsm', 
    sources = hsmsources)

setup(
    name = 'SimpleQmap',
    version='%s' % SimpleQmap.__version__,
    description='Calculator of quantum maps',
    author='Yasutaka Hanada',
    author_email='hanada1985@gmail.com',
    url='http://www.abc.com',
    packages=['SimpleQmap',"SimpleQmap.ctypes_wrapper"],
    ext_package='SimpleQmap.shared',
    ext_modules = [hsm_module]
)
