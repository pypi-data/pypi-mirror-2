from setuptools import setup, find_packages

setup(name='pydenji',
      version='0.2.1',
      description='Dependency Injection Toolkit',
      long_description="""
      Dependency Injection Toolkit.

      Enables easy dependency injection and declarative configuration for
      Python projects. While inspired by projects such as Spring Framework
      or Ruby's DIM, it is designed to be unobtrusive. It doesn't require
      modification in your business code to be employed; it can just be used in
      the outer layer, where configuration is actually needed.

      Small additional tools to help with configuration management are provided
      and can be used when and where are really fit.
      """,
      author='Alan Franzoni',
      license='APL 2.0',
      keywords='dependency injection inversion control ioc container',
      author_email='username@franzoni.eu',
      url='http://pydenji.franzoni.eu',
      packages=find_packages(exclude=["test", "pydenji_integration_test"])
     )
