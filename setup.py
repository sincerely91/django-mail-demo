from setuptools import setup, find_packages


setup(
    name = "django-mailify",
    version = __import__("mailify").__version__,
    description = "Enhance the builtin Django mail functionality to " + \
        "include task queueing or deferment.",
    author = "Keith Hall",
    author_email = "code@keith.io",
    url = "https://keithio.github.com/django-mailify",
    packages = find_packages(),
    classifiers = [
        "Environment :: Web Environment"
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django"
    ],
    include_package_data = True,
    zip_safe = False
)