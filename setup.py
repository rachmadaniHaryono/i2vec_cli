"""setup."""
import setuptools

description = "Use illustration2vec on cli"
try:
    long_description = open("README.rst").read()
except IOError:
    long_description = description

install_requires = (
    # TODO fix requirement setup.
    # use requirements.txt for now>
)

setuptools.setup(
    name="i2vec_cli",
    version="0.1.0",
    url="https://github.com/rachmadaniHaryono/i2vec_cli",

    author="Rachmadani Haryono",
    author_email="foreturiga@gmail.com",

    description=description,
    long_description=long_description,

    packages=setuptools.find_packages(),

    install_requires=install_requires,

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
