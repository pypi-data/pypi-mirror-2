from setuptools import setup, find_packages

setup(
    name='praekelt.recipe.deploy',
    version='0.0.7',
    description='Buildout recipe making versioned remote deploys trivial.',
    long_description = open('README.rst', 'r').read() + open('AUTHORS.rst', 'r').read() + open('CHANGELOG.rst', 'r').read(),
    author='Praekelt Foundation',
    author_email='dev@praekelt.com',
    license='BSD',
    url='http://github.com/praekelt/praekelt.recipe.deploy',
    packages = find_packages(),
    install_requires = [
        'zc.recipe.egg',
        'fabric==0.9.4',
    ],
    include_package_data=True,
    classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Framework :: Buildout",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
    entry_points = {'zc.buildout': ['default = praekelt.recipe.deploy:Deploy']},
)
