from distutils.core import setup
import os

local_file = lambda f: \
    open(os.path.join(os.path.dirname(__file__), f)).read()

setup(
  name = 'CustomOperators',
  packages = ['CustomOperators'],
  version = '0.4',
  license='MIT',
  description = 'Custom operator implementation in Python',
  long_description=local_file('README.rst'),
  author = 'Qkrisi',
  author_email = 'qruczkristof@gmail.com',
  url = 'https://github.com/qkrisi/python-custom-operators',
  download_url = 'https://github.com/qkrisi/python-custom-operators/archive/v_0_4.tar.gz',
  keywords = ['Operator'],
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Code Generators',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ]
)
