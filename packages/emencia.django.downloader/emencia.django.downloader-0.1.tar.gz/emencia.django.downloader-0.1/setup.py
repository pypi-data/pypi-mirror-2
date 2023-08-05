from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='emencia.django.downloader',
      version=version,
      description="Downloader app like dl.free.fr in django",
      long_description=open('README.rst').read() + '\n' +
                       open(os.path.join('docs', 'HISTORY.txt')).read(),
      keywords='',
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'License :: OSI Approved :: GNU Affero General Public License v3',
          ],

      author='Philippe Lafaye',
      author_email='lafaye@emencia.com',
      url='http://www.emencia.fr',

      license='GNU Affero General Public License v3',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['emencia', 'emencia.django'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
