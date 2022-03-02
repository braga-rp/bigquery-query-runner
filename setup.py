import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE/"README.md").read_text()


setup(
    name='bigquery-query-runner',
    version='1.0.0',
    packages=find_packages(),
    author="Pedro Rangel Braga",
    url='https://github.com/braga-rp/bigquery-query-runner',
    license='MIT',
    description=README,
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    setup_requires=['wheel', 'twine'],
    tests_require=[
        "pytest==6.2.2"
    ],
    install_requires=[
        "PyGithub==1.54.1",
        "jinjasql==0.1.8",
        'google-cloud-bigquery==1.25.0',
        "smart-open[all]==4.2.0",
        "click==7.1.2"
    ],
    entry_points={
        'console_scripts': [
            'run-query=bigquery_query_runner.main:main'
        ]
    }
)
