from setuptools import setup, find_packages


setup(
    name='django-templateaddons',
    version='0.1',
    url='http://bitbucket.org/benoitbryon/django-templateaddons/',
    author='Benoit Bryon',
    author_email='benoit@marmelune.net',
    license='LICENSE',
    description = "A set of tools for use with templates of the Django " \
                  "framework: additional template tags, context processors " \
                  "and utilities for template tag development.",
    long_description=open('README.txt').read(),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Framework :: Django',
    ],
    packages=find_packages(),
    include_package_data = True,
)
