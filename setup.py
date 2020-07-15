from setuptools import setup

install_dependencies = [
      'numpy >= 1.18',
      'pandas >= 1.0',
      'geopandas >= 0.7'
]

test_dependencies = [
      'pytest'
]

setup(name='gdutils',
      version='0.0.1',
      description='A collection of geodata tools',
      url='https://github.com/KeiferC/gdutils',
      author='@KeiferC',
      license='MIT', 
      packages=['gdutils'],
      install_requires=install_dependencies,
      tests_requires=test_dependencies,
      test_suite='pytest')
