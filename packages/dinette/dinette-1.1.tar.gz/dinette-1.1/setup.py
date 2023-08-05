import os
from setuptools import setup, find_packages

setup(
    name='dinette',
    description='Dinette is a forum application in the spirit of PunBB.',
    keywords='django, forum',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    version="1.1",
    author="Agiliq Solutions",
    author_email="hello@agiliq.com",
    long_description=
    """
        Dinette Forum
        ---------------
        
        The name
        ==============
        Dinette is a composition by Django Reinhardt. I haven't personally heard it, but I believe that like everything
        built with or by Django it is going to be superb.
        
        Overview.
        ===========
        
        Dinette is a forum built with Django. It uses the PunBB philosophy of being lightweight, but functional. Additionaly
        it takes
        the HTML wholesale from PunBB. Like PunBB, it is GPL licensed.
        
        Why Another?
        ================
        There are a lot of existing forum applications for Django, so why another.
        In our belief, there is no forum application, (Apart from that bundled with Ellington)
        of quality comparable to that available to PHP. Djorum is not there yet, but Usware plans
        to provide long term support for it,
        and continue to develop this depending on community support.
        
        Features
        ===============
        1. Fully reuable, plug and play in your existing site.
        2. Plays well with other Django components, like auth and django-registration, admin.
        3. Support BBCode
        4. Supports File attachement.
        5. Supports image attachment
        6. Supports supercategories, categories, and topic. (Upto 3 levels of nesting).
        7. Support groups and limited visibility.
        8. Supports Karma
        9. Supports Ranks
        10.Supports announcements.
        11. Supports RSS
        And many, many others.
        
        Why use this
        ==================
        Why use this instead of say PubBB?
        
        This integrates tightly with other Django subsystems, including Admin, User and Groups.
        
        
        How to use it.
        ================
        1. Put it into your existing Django project.
        2. Syncdb
        3. Make your registration system create a DinetteUserProfile object for each user who is going to use Dinette.
        4. Create supercategories, categories and categories.
        5. Play.
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
