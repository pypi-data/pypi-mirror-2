from setuptools import setup, find_packages
import os

CLASSIFIERS = []

setup(
    author="Christopher Glass",
    author_email="tribaal@gmail.com",
    name='django-shop-simplecategories',
    version='0.0.3',
    description='A simple to use product categories module for django SHOP',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    url='http://www.django-shop.org/',
    license='BSD License',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=[
        'Django>=1.2',
        'django-shop',
    ],
    packages=find_packages(exclude=["example", "example.*"]),
    include_package_data=True,
    zip_safe = False
)

