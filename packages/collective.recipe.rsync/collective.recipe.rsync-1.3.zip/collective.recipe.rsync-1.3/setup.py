
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
    name='collective.recipe.rsync',
    version='1.3',
    description='Buildout recipe to copy data from one place to another.',
    long_description=read('README.txt') + read('docs/HISTORY.txt'),
    classifiers=[
      'Framework :: Buildout',
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Build Tools',
      'Topic :: Software Development :: Libraries :: Python Modules',
      'License :: OSI Approved :: Zope Public License',
      ],
    author='Alex Clark',
    author_email='aclark@aclark.net',
    url=('http://svn.plone.org/svn/collective/buildout/'
        'collective.recipe.rsync/'),
    license='ZPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=[
        'collective',
        'collective.recipe'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'zc.buildout'],
    entry_points={
        "zc.buildout":
            ["default = %s" % 'collective.recipe.rsync:Recipe']},
    tests_require=['zope.testing', 'zc.buildout']
    )
