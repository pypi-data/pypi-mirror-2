from setuptools import setup
import os

setup(name="pmxbot",
    version="1004-beta12",
    packages=["pmxbot", "pmxbotweb",],
    package_data={'pmxbot' : ["popquotes.sqlite",],
		'pmxbotweb' : ["templates/*.html", "templates/pmxbot.png",],
		},
    entry_points={
            'console_scripts' : 
'''
pmxbot=pmxbot.pmxbot:run
pmxbotweb=pmxbotweb.pmxbotweb:run
'''
    },
    install_requires=[
        "pyyaml",
        "python-irclib",
        "simplejson",
        "httplib2",
        "feedparser",
		#for viewer
		"jinja2",
		"cherrypy",
    ],
    description="IRC bot - full featured, yet extensible and customizable",
    license = 'MIT',
    author="You Gov, Plc. (jamwt, mrshoe, cperry, chmullig, and others)",
    author_email="open.source@yougov.com",
    maintainer = 'chmullig',
    maintainer_email = 'chmullig@gmail.com',
    url = 'http://bitbucket.org/yougov/pmxbot',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Communications :: Chat',
        'Topic :: Communications :: Chat :: Internet Relay Chat',
		'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    long_description = open(os.path.join(os.path.dirname(__file__), 'README')).read(),
    )
    
