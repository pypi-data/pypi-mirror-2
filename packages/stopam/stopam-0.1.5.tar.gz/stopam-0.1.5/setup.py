from distutils.core import setup
import stopam

setup(name='stopam',
      version=stopam.VERSION,
      description='A python client for the stopam.com spam prevention service',
      author='Emil Ivanov',
      author_email='emil.vladev@gmail.com',
      url='http://stopam.com/',
      packages=['stopam'],
      license='MIT')