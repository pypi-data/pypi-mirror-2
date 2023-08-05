from distutils.core import setup, Extension

setup(name='csorteddict',
    version='0.2',
    ext_modules=[Extension('csorteddict', ['csorteddict.c'])],

    author="Jason Scheirer",
    author_email="jason.scheirer@gmail.com",
    url="http://bitbucket.org/jasonscheirer/sorteddict/",
    description="Key-sorted (balanced tree) dictionary store implemented in C",
    license="BSD",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: POSIX :: BSD",
        "Programming Language :: C",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries"
    ],
    download_url="http://bitbucket.org/jasonscheirer/sorteddict/get/0.2.zip"
)
