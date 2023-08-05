from setuptools import setup, find_packages

version = __import__('insertblocks').__version__

setup(
    name = 'django-insertblocks',
    version = version,
    description = 'Django Insert Blocks',
    author = 'Jonas Obrist',
    author_email = 'jonas.obrist@divio.ch',
    url = 'http://github.com/ojii/django-insertblocks',
    packages = find_packages(),
    zip_safe=False,
)