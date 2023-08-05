from setuptools import setup, find_packages

setup(
    name = "django_divan",
    version = "0.2.2",
    url = 'http://github.com/threadsafelabs/django_divan',
    license = 'BSD',
    description = "User-definable schemas for Django.",
    author = 'Jonathan Lukens',
    author_email = 'jonathan@threadsafelabs.com',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
