from setuptools import setup, find_packages

setup(
    name='simpleencode',
    version=__import__('simpleencode').__version__,
    description='simple encode decode with a private key, based on the '
                'base64 encode and decode.',
    long_description=open('docs/overview.txt').read(),
    author='Doug Napoleone',
    author_email='doug.napoleone@gmail.com',
    url='http://code.google.com/p/python-simpleencode/',
    license = 'BSD License',
    platforms = ['any'],
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ],
    include_package_data=True,
    zip_safe=True,
)
