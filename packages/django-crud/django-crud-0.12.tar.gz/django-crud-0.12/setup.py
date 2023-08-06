from setuptools import setup, find_packages

setup(
    name='django-crud',
    version='0.12',
    description='CRUD application for Django',
    author='Sergey Klimov',
    author_email='sergey.v.klimov@gmail.com',
    url='http://github.com/darvin/django-crud/',
    packages=find_packages(exclude=['examples', 'examples.*']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    zip_safe=False,
)
