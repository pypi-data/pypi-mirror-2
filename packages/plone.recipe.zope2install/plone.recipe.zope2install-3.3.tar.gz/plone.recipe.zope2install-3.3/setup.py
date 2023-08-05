import os
from setuptools import setup, find_packages

name = "plone.recipe.zope2install"
version = '3.3'


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
        read('README.txt')
        + '\n' +
        read('CHANGES.txt'))

setup(
    name=name,
    version=version,
    author="Hanno Schlichting",
    author_email="hannosch@plone.org",
    description="ZC Buildout recipe for installing Zope 2.",
    long_description=long_description,
    license="ZPL 2.1",
    keywords="zope2 buildout",
    url='http://svn.plone.org/svn/collective/buildout/' + name,
    classifiers=[
      "License :: OSI Approved :: Zope Public License",
      "Framework :: Buildout",
      "Framework :: Plone",
      "Framework :: Zope2",
      "Programming Language :: Python",
      ],
    packages=find_packages('src'),
    include_package_data=True,
    package_dir={'': 'src'},
    namespace_packages=['plone', 'plone.recipe'],
    install_requires=['zc.buildout', 'setuptools'],
      extras_require=dict(
            test=[
                  'zope.testing',
                 ]),
    zip_safe=False,
    entry_points={'zc.buildout': ['default = %s:Recipe' % name]},
    )
