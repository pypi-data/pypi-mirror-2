import os

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

import os

version = '0.4'

setup(name='djangopypi',
      version=version,
      description="A Django application that emulates the Python Package Index.",
      long_description=open(os.path.join('docs', "README")).read() + "\n\n" +
                       open(os.path.join('docs', 'Changelog')).read() + "\n\n" +
                       open(os.path.join('docs', 'TODO')).read(),
      classifiers=[
        "Framework :: Django",
        "Development Status :: 4 - Beta",
        #"Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Topic :: System :: Software Distribution",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",],
      keywords='django pypi packaging index',
      author='Ask Solem',
      author_email='askh@opera.com',
      maintainer='Benjamin Liles',
      maintainer_email='benliles@gmail.com',
      url='http://github.com/benliles/chishop',
      license=open(os.path.join("docs", "LICENSE")).read(),
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'django>=1.0',
          'docutils',],
      )
