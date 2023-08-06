import os
from setuptools import setup
from pyyaru import VERSION

f = open(os.path.join(os.path.dirname(__file__), 'README'))
readme = f.read()
f.close()

setup(
    name='pyyaru',
    version=".".join(map(str, VERSION)),
    description='Python interface for ya.ru blog service API.',
    long_description=readme,
    author="Igor 'idle sign' Starikov",
    author_email='idlesign@yandex.ru',
    url='http://github.com/idlesign/pyyaru',
    packages=['pyyaru'],
    include_package_data=True,
    install_requires=['setuptools'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
