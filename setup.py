"""setup."""
# NOTE:
# install_requires removed right now
# because can't install dependency link on html-table-parser-python3.
# if html-table-parser-python3 already on pypi,
# then move required package from requirements.txt to here.
# right now install required package with `pip install -r requirements.txt`
import setuptools

description = "Use illustration2vec on cli"
try:
    long_description = open("README.rst").read()
except IOError:
    long_description = description


setuptools.setup(
    name="i2vec_cli",
    version="0.1.1",
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
        'console_scripts': ['i2vec-cli=i2vec_cli.__main__:main'],
    },
    zip_safe=False,
    # metadata for upload to PyPI
    # taken and modified from http://setuptools.readthedocs.io/en/latest/setuptools.html
    # see above for author, author_email and description
    license="MIT License",
    keywords="illustration2vec cli",
)
