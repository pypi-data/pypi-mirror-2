import os.path
from setuptools import setup, find_packages

def read(fname):
        return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='htmlfilter',
      version='0.2',
      description="White list HTML filter",
      long_description=read('README'),
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Markup :: HTML',
      ],
      keywords='html, filter, white list, parser, clean, tags',
      author='Samuel Adam',
      author_email='samuel.adam@gmail.com',
      url='http://github.com/samueladam/htmlfilter',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      )
