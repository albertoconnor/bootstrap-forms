
# Use setuptools if we can
try:
    from setuptools.core import setup
except ImportError:
    from distutils.core import setup

setup(
    name='bootstrap_forms',
    version="0.0.1",
    description='',
    long_description='',
    author='Albert O\'Connor',
    author_email='info@albertoconnor.ca',
    url='http://albertoconnor.ca',
    download_url='',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
    ],
    packages=[
        'bootstrap_forms',
    ],
)
