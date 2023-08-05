"""
Module to automatically build admin function runner
"""
from distutils.core import setup
setup(name='adminfuncs',
      version = '0.1',
      license = 'BSD',
      description = "Admin Function Runner",
      long_description = __doc__,
      author = "Brandon Thomson",
      author_email = 'brandon.j.thomson@gmail.com',
      py_modules = ['adminfuncs'],
      install_requires = [
        'werkzeug',
      ],
      classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      )
