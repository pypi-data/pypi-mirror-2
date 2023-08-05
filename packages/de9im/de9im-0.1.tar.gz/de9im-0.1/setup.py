from setuptools import setup, find_packages
import sys, os

version = '0.1'
text = open('README.txt').read()

setup(name='de9im',
      version=version,
      description="Dimensionally  Extended 9-Intersections Matrix utilities",
      long_description=text,
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: GIS'
      ],
      keywords='gis computational geometry',
      author='Sean Gillies',
      author_email='sean.gillies@gmail.com',
      url='http://bitbucket.org/sgillies/de9im/',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
