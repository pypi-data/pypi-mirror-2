from distutils.core import setup
from bertlet import __version__

version = __version__

setup(
    name='bertlet',
    version=version,
    description='BERT-RPC using Eventlet',
    author='Jared Kuolt',
    author_email='luckythetourist@gmail.com',
    url='http://github.com/luckythetourist/bertlet',
    packages=['bertlet'],
    license='MIT License',
    platforms=['any'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python', 
        'Topic :: Software Development', 
        'Topic :: Software Development :: Libraries', 
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
