from distutils.core import setup

all_packages = ['pytilities', 
                'pytilities.delegation', 
                'pytilities.event',
                'pytilities.event.test',
                'pytilities.geometry',
                'pytilities.geometry.test',
                'pytilities.overloading',
                'pytilities.overloading.test',
                'pytilities.test']

setup(
    name = 'pytilities',
    packages = all_packages,
    provides = all_packages,
    version = '0.1.1',
    description = 'A collection of python coding utilities',
    author = 'Tim Diels',
    author_email = 'limyreth@users.sourceforge.net',
    url = 'http://pytilities.sourceforge.net',
    keywords = ['utility', 'library', 'delegation', 'event', 'overloading'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        #TODO: does it work on py3? or any of the other versions?
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6', 
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    long_description = '''\
    pytilities is a utility library for developers.

    It has the following features:

        - delegation: decorate classes with attributes that are delegated to a
        target object without having to write those attributes on the decorating
        class

        - event dispatching: Observer/Listener like event dispatching with wrappers
        for hiding events on dispatchers and combining dispatchers

        - function overloading

        - various: a NumberType (anything numeric), a mangle function, ...

    Tested on python 2.6, it may work on other versions as well.
    '''
)
