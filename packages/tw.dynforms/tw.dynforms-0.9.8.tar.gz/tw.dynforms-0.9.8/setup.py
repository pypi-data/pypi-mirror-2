import os
import sys

from setuptools import setup, find_packages

execfile(os.path.join("tw", "dynforms", "release.py"))

setup(
    name='tw.dynforms',
    version=__VERSION__,
    description=__DESCRIPTION__,
    author=__AUTHOR__,
    author_email=__EMAIL__,
    url=__URL__,
    install_requires=[
        "tw.forms > 0.9.7",
        "Genshi",
        "SQLAlchemy >= 0.4",
        ],
    packages=find_packages(exclude=['ez_setup', 'tests']),
    namespace_packages = ['tw'],
    zip_safe=False,
    include_package_data=True,
    test_suite = 'nose.collector',
    entry_points="""
        [toscawidgets.widgets]
        # Use 'widgets' to point to the module where widgets should be imported
        # from to register in the widget browser
        widgets = tw.dynforms
        # Use 'samples' to point to the module where widget examples
        # should be imported from to register in the widget browser
        samples = tw.dynforms.samples
        # Use 'resources' to point to the module where resources
        # should be imported from to register in the widget browser
        #resources = toscawidgets.widgets.dynforms.resources
    """,
    keywords = [
        'toscawidgets.widgets',
    ],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Environment :: Web Environment :: ToscaWidgets',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Widget Sets',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
