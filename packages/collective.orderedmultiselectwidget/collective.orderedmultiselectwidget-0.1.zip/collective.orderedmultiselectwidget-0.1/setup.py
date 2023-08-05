from setuptools import setup, find_packages

import os
def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.1'

long_description = (
    read('README.txt')
    + '\n' +
    read('docs/HISTORY.txt')
    )

setup(
    name='collective.orderedmultiselectwidget',
    version=version,
    description="Provides SecureOrderedMultiSelectWidget which fixes an acquisition bug in OrderedMultiSelectWidget in zope.app.form.",
    long_description=long_description,
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        ],
    keywords='orderedmultiselectwidget',
    author='JC Brand, Syslab.com GmbH',
    author_email='brand@syslab.com',
    url='',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',    
    ],
    entry_points="""
        [z3c.autoinclude.plugin]
        target = plone
    """,
    )
