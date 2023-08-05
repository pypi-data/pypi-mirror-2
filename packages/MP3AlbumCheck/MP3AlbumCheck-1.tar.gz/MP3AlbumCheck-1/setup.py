from setuptools import setup, find_packages
import sys, os

version = '1'

setup(name='MP3AlbumCheck',
      version=version,
      description="Checks a directory of MP3s to ensure it matches its CD equivilent",
      long_description="""\
Given a directory of MP3 files, MP3AlbumCheck will calculate a FreeDB/CDDB id of the directory and try to match it to an entry in the FreeDB/CDDB database. If there is a match, it will prompt to tag the album appropriately.""",
      classifiers=[
        "Environment :: Console",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
      ],
      keywords='mp3 album freedb cddb eyed3',
      author='Joe Topjian',
      author_email='joe@terrarum.net',
      url='http://terrarum.net/mp3albumcheck.html',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
      ],
      entry_points= {
          'console_scripts': [
                'mp3albumcheck = mp3albumcheck.cli:main'
          ]
      },
      )
