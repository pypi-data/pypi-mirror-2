from setuptools import setup, find_packages
from annotator import __version__, __license__, __author__

setup(
    name = 'annotator',
    version = __version__,
    packages = find_packages(),
    install_requires = open('./requirements.txt').readlines(),

    # metadata for upload to PyPI
    author = __author__,
    author_email = 'annotator@okfn.org',
    description = 'Inline web annotation application and middleware using javascript and WSGI',
    long_description = 'Inline javascript-based web annotation library. Package includeds a database-backed annotation store with RESTFul (WSGI-powered) web-interface.',
    license = __license__,
    keywords = 'annotation web javascript',
    url = 'http://github.com/nickstenning/annotator-store-py',
    download_url = 'http://github.com/nickstenning/annotator-store-py',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points = '[paste.app_factory]\nstore = annotator.store:make_app',
)
