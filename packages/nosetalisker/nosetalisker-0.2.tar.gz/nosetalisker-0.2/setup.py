from setuptools import setup, find_packages

setup(
    name='nosetalisker',
    version='0.2',
    description='',
    long_description='',
    author='Andy McKay',
    author_email='andym@mozilla.com',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    install_requires=[r for r in open('requirements.txt')
                      if r.strip() and not r.startswith('#')],
    url='',
    include_package_data=True,
    entry_points='''
        [nose.plugins.0.10]
        talisker = nosetalisker:Talisker
        ''',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Testing',
        ],
    )
