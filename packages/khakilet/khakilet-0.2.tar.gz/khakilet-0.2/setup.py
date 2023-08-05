from setuptools import setup, find_packages

setup(name='khakilet',
      version='0.2',
      description='Python network library that uses greenlet, libev and libudns',
      author='Paul Colomiets',
      author_email='pc@gafol.net',
      url='http://khakilet.gafol.net',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        ],
      packages=find_packages(),
     )
