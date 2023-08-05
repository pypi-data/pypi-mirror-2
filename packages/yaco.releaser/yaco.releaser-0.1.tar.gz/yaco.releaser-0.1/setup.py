from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='yaco.releaser',
      version=version,
      description="Yaco addon to zest.releaser to include ticket referencce in commits",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules"
        ],
      keywords='',
      author='Pablo Caro Revuelta',
      author_email='pcaro@yaco.es',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['yaco'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'zest.releaser>3.0'
      ],
      entry_points={
      # -*- Entry points: -*-
      'zest.releaser.prereleaser.middle': [
        'commit_msg_sufix = yaco.releaser:sufix_commit_msg',
        ],
      'zest.releaser.postreleaser.middle': [
        'commit_msg_sufix = yaco.releaser:sufix_commit_msg',
        ],
      },
      )
