from setuptools import setup, find_packages

version = '2.0b4'

setup(name='plone.app.form',
      version=version,
      description="zope.formlib integration for Plone",
      long_description=open("README.txt").read() + "\n" + \
                       open("CHANGES.txt").read(),
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://pypi.python.org/pypi/plone.app.form',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages = ['plone', 'plone.app'],
      include_package_data=True,
      zip_safe=False,
      extras_require=dict(
        test=[
            'plone.memoize',
            'plone.app.content',
            'zope.annotation',
            'zope.publisher',
            'zope.testing',
            'Products.PloneTestCase',
        ],
        kss=[
            'kss.core',
            'plone.app.kss',
        ],
      ),
      install_requires=[
        'setuptools',
        'plone.locking',
        'plone.app.vocabularies',
        'zope.browser',
        'zope.component',
        'zope.event',
        'zope.formlib',
        'zope.i18n',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.lifecycleevent',
        'zope.schema',
        'zope.site',
        'zope.app.form',
        'Products.CMFCore',
        'Products.CMFDefault',
        'Acquisition',
        'DateTime',
        'Zope2',
      ],
      )
