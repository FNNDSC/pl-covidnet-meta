from setuptools import setup

setup(
    name='covidnet-meta',
    version='1.0.6',
    description='A ChRIS plugin that analyzes an upstream COVID prediction.json file and, if COVID infection inferred, will exit with an exception. This has the effect of coloring the node red in the DAG representation.',
    author='FNNDSC',
    author_email='dev@babyMRI.org',
    url='https://github.com/FNNDSC/pl-covidnet-',
    py_modules=['covidnet_meta'],
    install_requires=['chris_plugin'],
    license='MIT',
    entry_points={
        'console_scripts': [
            'covidnet_meta = covidnet_meta:main'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.'
    ],
    extras_require={
        'none': [],
        'dev': [
            'pytest~=7.1',
            'pytest-mock~=3.8'
        ]
    }
)
