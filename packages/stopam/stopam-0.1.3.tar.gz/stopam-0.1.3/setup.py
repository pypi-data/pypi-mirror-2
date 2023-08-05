from distutils.core import setup

setup(name='stopam',
      version='0.1.3',
      description='A python client for the stopam.com spam prevention service',
      author='Emil Ivanov',
      author_email='emil.vladev@gmail.com',
      url='http://stopam.com/',
      packages=['stopam'],
      scripts=['stopam_demo.py'],
      license='MIT')