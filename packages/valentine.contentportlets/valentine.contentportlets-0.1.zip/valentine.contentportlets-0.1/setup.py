from setuptools import setup, find_packages
import os

version = '0.1'

tests_require=['zope.testing']

setup(name='valentine.contentportlets',
      version=version,
      description="",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='plone',
      author='Sasha Vincic',
      author_email='sasha dot vincic at valentinwebsystems dot com',
      url='http://dev.plone.org/collective/browser/valentine.contentportlets/trunk',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['valentine', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        # -*- Extra requirements: -*-
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'valentine.contentportlets.tests.test_docs.test_suite',
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
