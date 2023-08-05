from distutils.core import setup

setup(
    name='longurl',
    version='0.0.1',
    author='matt wartell',
    author_email='mswbb@users.bitbucket.org',
    url = 'http://bitbucket.org/mswbb/python-longurl/overview',
    description='a wrapper for the LongURL expansion service at longurl.org',
    license = 'BSD',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
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
