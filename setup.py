"""setup."""
import setuptools

description = "Use illustration2vec on cli"
try:
    long_description = open("README.rst").read()
except IOError:
    long_description = description


install_requires = [
    'appdirs>=1.4.3',
    'click>=6.7',
    'Flask>=0.12.2',
    'peewee>=2.10.1',
    'Pillow>=4.2.1',
    'requests>=2.18.1',
    'structlog>=17.2.0',
]


setuptools.setup(
    name="i2vec_cli",
    version="0.2.0",
    url="https://github.com/rachmadaniHaryono/i2vec_cli",

    author="Rachmadani Haryono",
    author_email="foreturiga@gmail.com",

    description=description,
    long_description=long_description,

    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'console_scripts': [
            'i2vec-cli=i2vec_cli.__main__:main',
            'i2vec-cli-server=i2vec_cli.server:main',
        ],
    },
    install_requires=install_requires,
    zip_safe=False,
    # metadata for upload to PyPI
    # taken and modified from http://setuptools.readthedocs.io/en/latest/setuptools.html
    # see above for author, author_email and description
    license="MIT License",
    keywords="illustration2vec cli",
)
