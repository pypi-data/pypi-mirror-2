import os
from setuptools import setup, find_packages

setup(
    name='dinette',
    description='Dinette is a forum application in the spirit of PunBB.',
    keywords='django, forum',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    version="1.0",
    author="Agiliq Solutions",
    author_email="hello@agiliq.com",
    long_description=
    """
        Dinette is a forum built with Django. It uses the PunBB philosophy of being lightweight, but functional. Additionaly
        it takes the HTML wholesale from PunBB. Like PunBB, it is GPL licensed.
    """,
    classifiers = ['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: GNU General Public License (GPL)',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Internet :: WWW/HTTP',
                   'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
                   'Topic :: Internet :: WWW/HTTP :: WSGI',
                   'Topic :: Software Development :: Libraries :: Application Frameworks',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   ],
    url="http://www.agiliq.com/",
    license="GPL",
    platforms=["all"],
)
