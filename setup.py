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
    url='https://github.com/cbefus/Eynnyd',
    license='MIT License',
    install_requies=[
        'arrow==0.14.4',
        'optional.py==1.0.0'
    ],
    packages=find_packages(exclude=('test')),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    keywords='wsgi web framework api rest http',
    python_requires='>=3.5'
)