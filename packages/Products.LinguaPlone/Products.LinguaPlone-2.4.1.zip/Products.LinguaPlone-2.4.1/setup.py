from setuptools import setup, find_packages
import os.path

version = '2.4.1'

setup(name='Products.LinguaPlone',
      version=version,
      description="Manage and maintain multilingual content that integrates seamlessly with Plone.",
      long_description=".. contents::\n\n" +
                        open(os.path.join("Products", "LinguaPlone", "README.txt")).read() + "\n" +
                        open(os.path.join("Products", "LinguaPlone", "FAQ.txt")).read() + "\n" +
                        open(os.path.join("Products", "LinguaPlone", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
      ],
      keywords='Zope CMF Plone multilingual translation',
      author='Jarn (formerly Plone Solutions)',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://svn.plone.org/svn/plone/LinguaPlone/trunk',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      download_url='http://plone.org/products/linguaplone',
      install_requires=[
        'setuptools',
        'plone.browserlayer',
        'plone.app.layout >= 1.1.4',
      ],
)
