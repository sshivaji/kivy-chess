from distutils.core import setup, Extension
import platform

args=[]
if '64bit' in platform.architecture():
  args.append('-DIS_64BIT')

module1 = Extension('pydgtnix',
                    sources = ['dgtnix.c'],extra_compile_args=args)

setup (name = 'pydgtnix',
       version = '0.1',
       description = 'Python dgtnix',
       ext_modules = [module1])
