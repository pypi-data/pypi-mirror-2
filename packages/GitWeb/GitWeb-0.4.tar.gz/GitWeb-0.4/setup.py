import os

from setuptools import setup, find_packages

setup(name='GitWeb',
      version='0.4',
      description='WSGI application to serve a git repository',
      long_description=open('README.txt').read(),
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Gael Pasgrimaud',
      author_email='gael@gawel.org',
      url='https://github.com/gawel/GitWeb',
      licence='GPL',
      keywords='web',
      py_modules = ['gitweb', 'subprocessio'],
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=['WebOb'],
      tests_require=[],
      entry_points = """\
      [paste.app_factory]
      main = gitweb:make_dir_app
      dir = gitweb:make_dir_app
      repo = gitweb:make_app
      """,
      )

