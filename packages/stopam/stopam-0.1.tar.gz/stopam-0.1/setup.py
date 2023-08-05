from distutils.core import setup

setup(name='stopam',
      version='0.1',
      description='A python client for the stopam.com spam prevention service',
      author='Emil Ivanov',
      author_email='emil.vladev@gmail.com',
      url='stopam.com',
      packages=['stopam'],
      scripts=['stopamdemo'],
      license='MIT')