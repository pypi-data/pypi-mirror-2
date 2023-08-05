from setuptools import setup, find_packages
import os

version = open(os.path.join("Products", "ATPhoto", "version.txt")).read().strip()

setup(name='Products.ATPhoto',
      version=version,
      description="ATPhoto is a product to manage photos in your Plone site",
      long_description=open(os.path.join("Products", "ATPhoto", "doc", "README.txt")).read().decode('UTF8').encode('ASCII', 'replace') + '\n' +
                       open(os.path.join("Products", "ATPhoto", "doc", "HISTORY.txt")).read() +
                       open(os.path.join("Products", "ATPhoto", "doc", "AUTHORS.txt")).read().decode('UTF8').encode('ASCII', 'replace') + '\n',
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='plone ATPhoto',
      author='Russ Ferriday',
      author_email='russ@topia.com',
      url='https://svn.plone.org/svn/collective/Products.ATPhoto',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
