from setuptools import setup

setup(name='gdutils',
      version='0.0.1',
      description='A collection of geodata tools',
      url='https://github.com/KeiferC/gdutils',
      author='@KeiferC',
      license='MIT', 
      packages=['gdutils'],
      install_requires=['numpy >= 1.18',
                        'pandas >= 1.0',
                        'geopandas >= 0.7'])
