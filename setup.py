from setuptools import setup, find_packages


setup(
    name = "django-mailify",
    version = "0.1.0alpha2",
    description = "Enhance the builtin Django mail functionality to " + \
        "include task queueing or deferment.",
    author = "Keith Hall",
    author_email = "code@keith.io",
    url = "https://keithio.github.com/django-mailify",
    packages = find_packages(),
    classifiers = [
        "Environment :: Web Environment",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python"
    ],
    include_package_data = True,
    zip_safe = False
)