from setuptools import setup, find_packages
import os

version = '0.1b2'

long_desc = open(os.path.join("collective", "contentgroup", "README.txt")).read() \
    + "\n" + open(os.path.join("docs", "HISTORY.txt")).read()

setup(name='collective.contentgroup',
      version=version,
      description="Plone add-on that allows to associate users groups with content objects",
      long_description=long_desc,
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone groups users',
      author="Rafael Oliveira",
      author_email="rafaelbco@gmail.com",
      url="http://svn.plone.org/svn/collective/collective.contentgroup",
      license="GPL",
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools', 
      ],
      entry_points='',
)
