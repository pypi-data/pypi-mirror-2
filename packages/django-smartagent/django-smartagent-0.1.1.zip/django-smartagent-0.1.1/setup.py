from setuptools import setup, find_packages

setup(
    name = 'django-smartagent',
    version = '0.1.1',
    description = 'django-smartagent is the fastest and most complete user agent parser',
    long_description = open('README.rst').read(),
    keywords = 'django apps',
    license = 'BSD License',
    author = 'James Pacileo',
    author_email = 'jamespacileo@gmail.com',
    url = 'http://github.com/jamespacileo/django-smartagent/',
    dependency_links = [],
    classifiers = [
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages = ['smartagent'],
    #packages = find_packages(exclude=['ez_setup', 'test_project']),
    include_package_data = True,
    zip_safe = False,
    package_data = {
        'smartagent': ['smartagent/agents_basic.pkl',],
      },
)