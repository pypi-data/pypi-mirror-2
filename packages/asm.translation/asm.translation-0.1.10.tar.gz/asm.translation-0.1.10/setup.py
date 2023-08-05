from setuptools import setup, find_packages


setup(name='asm.translation',
      version='0.1.10',
      description="Multi-lingual content for Assembly CMS",
      author="Webcrew",
      author_email="web@assembly.org",
      url="",
      license="proprietary",
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=['ZODB3',
                        'asm.cms',
                        'setuptools',
                        'grok',
                        'zope.interface',
                        'zope.schema'])
