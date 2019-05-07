from distutils.core import setup

setup(name='Simple-LSH',
      version='1.0',
      description='Python Distribution Utilities',
      author='Mehmet Akdel',
      author_email='akdel.mehmet@gmail.com',
      url='https://github.com/akdel/local-sensitivity-hashing',
      packages=['LSH'],
      install_requires=["numpy", "numba"]
     )
