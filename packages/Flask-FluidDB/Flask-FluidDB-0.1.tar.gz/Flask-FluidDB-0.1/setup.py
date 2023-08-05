"""
Flask FluidDB
-------------

Description goes here...

Links
`````

* `documentation <http://packages.python.org/Flask%20FluidDB>`_
* `development version
  <http://bitbucket.org/aafshar/flask-fluiddb-main/get/tip.gz#egg=Flask-FluidDB-dev>`_


"""
from setuptools import setup


setup(
    name='Flask-FluidDB',
    version='0.1',
    url='http://bitbucket.org/aafshar/flask-fluiddb-main',
    license='MIT',
    author='Ali Afshar',
    author_email='aafshar@gmail.com',
    description='Fluiddb access for flask',
    long_description=__doc__,
    packages=['flaskext'],
    namespace_packages=['flaskext'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask', 'fom', 'httplib2'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
