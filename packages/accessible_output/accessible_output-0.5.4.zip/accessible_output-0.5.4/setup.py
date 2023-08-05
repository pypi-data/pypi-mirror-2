from setuptools import setup
from glob import glob

setup(
 name = 'accessible_output',
 author = 'Christopher Toth',
 author_email = 'q@qwitter-client.net',
 version = '0.5.4',
 url = 'http://www.qwitter-client.net',
 description = 'Library to provide speech and braille output to a variety of different screen readers and other accessibility solutions.',
 long_description = open('README.txt').read(),
 data_files = glob('lib'),
 package_dir = {'accessible_output':''},
 packages = ['accessible_output', 'accessible_output.braille', 'accessible_output.speech', 'accessible_output.braille.outputs', 'accessible_output.speech.outputs'],
 classifiers = [
  'Development Status :: 4 - Beta',
  'Intended Audience :: Developers',
  'Operating System :: Microsoft :: Windows',
  'Programming Language :: Python',
  'License :: OSI Approved :: MIT License',
'Topic :: Adaptive Technologies',
'Topic :: Software Development :: Libraries'
],
 install_requires = [
  #'pywin32',
]
)
