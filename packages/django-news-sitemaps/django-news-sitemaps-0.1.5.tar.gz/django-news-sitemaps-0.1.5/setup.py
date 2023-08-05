from setuptools import setup

setup(
    name = 'django-news-sitemaps',
    version = '0.1.5',
    description = 'Generates sitemaps compatible with the Google News schema',
    author = 'TWT Web Devs',
    author_email = 'webdev@washingtontimes.com',
    url = 'http://github.com/washingtontimes/django-news-sitemaps/',
    include_package_data = True,
    packages = ['news_sitemaps'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
    ]
)
