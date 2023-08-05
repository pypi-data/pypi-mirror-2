from setuptools import setup

setup(
      name='MicroApacheMonitor',
      version='0.1c1',
      author='James R. Cook',
      author_email='cookjr@users.sourceforge.net',
      install_requires=['pywin32'],
      packages=['mapachemon'],
      scripts=['bin/mapachemon_start.py', 'bin/mapachemon_start.bat', ],
      data_files=[('mapachemon', ['mapachemon/mapachemon.ico']),],
      url='http://sourceforge.net/projects/mapachemonitor/',
      license='LICENSE.txt',
      description='Windows system tray app for controlling MicroApache',
      long_description=open('README.txt').read(),
     )
