from distutils.core import setup
import eztv

setup(
    name="eztv",
    version=eztv.__version__,
    description="A screenscraper for http://eztv.it",
    author="Alexander Borgerth",
    author_email="alex.borgert@gmail.com",
    license="MIT/X",
    url="http://launchpad.net/pyeztv",
    packages=["eztv"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries'
    ],
)

