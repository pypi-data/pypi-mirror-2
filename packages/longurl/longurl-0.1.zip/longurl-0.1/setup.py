from distutils.core import setup

setup(
    name='longurl',
    version='0.1',
    author='matt wartell',
    author_email='mswbb@users.bitbucket.org',
    url = 'http://bitbucket.org/mswbb/python-longurl/overview',
    description='a wrapper for the LongURL expansion service at longurl.org',
    long_description="""A python binding for the URL expansion service
        provided by longurl.org. The single file module export a LongURL class
        suitable for import into another python script and also contains a
        command line interface for the library service when run as __main__""",
    license = 'BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    py_modules=['longurl'],
)
