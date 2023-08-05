from setuptools import setup, find_packages

version = '2.0b2'

setup(name='plone.app.iterate',
      version=version,
      description="check-out/check-in staging for Plone",
      long_description=\
          open("README.txt").read() + "\n" + \
          open("CHANGES.txt").read(),
      classifiers=[
        "Framework :: Zope2",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Kapil Thangavelu',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://pypi.python.org/pypi/plone.app.iterate',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages = ['plone', 'plone.app'],
      include_package_data=True,
      zip_safe=False,
      extras_require=dict(
        test=[
            'Products.PloneTestCase',
        ]
      ),
      install_requires=[
          'setuptools',
          'plone.locking',
          'plone.memoize',
          'zope.annotation',
          'zope.component',
          'zope.event',
          'zope.i18nmessageid',
          'zope.interface',
          'zope.schema',
          'zope.viewlet',
          'Acquisition',
          'DateTime',
          'Products.Archetypes',
          'Products.CMFCore',
          'Products.CMFEditions',
          'Products.CMFPlacefulWorkflow',
          'Products.DCWorkflow',
          'Products.statusmessages',
          'ZODB3',
          'Zope2',
      ],
      )
