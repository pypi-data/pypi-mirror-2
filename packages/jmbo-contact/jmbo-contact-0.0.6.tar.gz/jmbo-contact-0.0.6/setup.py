from setuptools import setup, find_packages

setup(
    name='jmbo-contact',
    version='0.0.6',
    description='Jmbo contact form app.',
    long_description = open('README.rst', 'r').read(),
    author='Praekelt International',
    author_email='dev@praekelt.com',
    license='BSD',
    url='http://github.com/praekelt/jmbo-contact',
    packages = find_packages(),
    install_requires = [
        'django-preferences',
        'jmbo',
    ],
    include_package_data=True,
    classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
