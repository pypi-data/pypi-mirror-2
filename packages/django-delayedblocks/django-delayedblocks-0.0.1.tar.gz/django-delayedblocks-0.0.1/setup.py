from setuptools import setup, find_packages

version = __import__('delayedblocks').__version__

setup(
    name = 'django-delayedblocks',
    version = version,
    description = 'Django Delayed Blocks',
    author = 'Jonas Obrist',
    author_email = 'jonas.obrist@divio.ch',
    url = 'http://github.com/ojii/django-delayedblocks',
    packages = find_packages(),
    zip_safe=False,
)