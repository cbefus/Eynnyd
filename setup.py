from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='eynnyd',
    version='0.0.1',
    description='A light-weight wsgi web framework',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Chad Befus',
    author_email='crbefus@gmail.com',
    url='https://github.com/cbefus/Eynnyd.py',
    license='MIT License',
    packages=find_packages(exclude=('test')),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries'
    ],
    keywords='wsgi web framework',
    python_requires='>=3.2'
)