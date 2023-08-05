from setuptools import setup, find_packages
import os

version = '1.1'

setup(name='snd.PloneMemberChannel',
      version=version,
      description="Patch for Singing and Dancing that allows sending mails to plone members too.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("snd/PloneMemberChannel/HISTORY.txt")
                            ).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='singing dancing channel',
      author='Zest software',
      author_email='v.pretre@zestsoftware.nl',
      url='http://svn.plone.org/svn/plone/plone.example',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['snd'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
