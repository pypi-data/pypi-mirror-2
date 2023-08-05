from distutils.core import setup
setup(name='reactorauth',
      version='0.2',
      description=""" Set of decorators for authorization + small list
       of example checks for pylons""",
      author='Marcin Lulek',
      author_email='info@webreactor.eu',
      license='BSD',
      packages = ['reactorauth','reactorauth.pylonslib'],
      install_requires=["decorator>=2.3.2"]
      )