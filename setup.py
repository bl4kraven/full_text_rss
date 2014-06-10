from setuptools import setup, find_packages
from full_text_rss import __version__

try:
    from pypandoc import convert

    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

if __name__ == '__main__':
    project_name = "full_text_rss"
    setup(
        name=project_name,
        version=__version__,
        author="lbzhung",
        license="GNU AGPL",
        url="https://github.com/lbzhung/full_text_rss",
        packages=find_packages(),
        long_description=read_md('README.md'),
    )
