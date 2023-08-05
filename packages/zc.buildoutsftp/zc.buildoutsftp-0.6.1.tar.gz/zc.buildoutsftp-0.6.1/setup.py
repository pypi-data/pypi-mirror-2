from setuptools import setup, find_packages

name='zc.buildoutsftp'
setup(
    name=name,
    version = "0.6.1",
    author = "Jim Fulton",
    author_email = "jim@zope.com",
    description = "Specialized zc.buildout plugin to add sftp support.",
    long_description = open('README.txt').read(),
    license = "ZPL 2.1",
    keywords = "buildout",
    url='http://www.python.org/pypi/'+name,

    packages = find_packages('src'),
    include_package_data = True,
    package_dir = {'':'src'},
    namespace_packages = ['zc'],
    install_requires = ['paramiko', 'setuptools'],
    zip_safe=False,
    entry_points = {
        'zc.buildout.extension': ['default = %s.buildoutsftp:install' % name],
        'zc.buildout.unloadextension': ['default = %s.buildoutsftp:unload' % name],
        },
    classifiers = [
       'Framework :: Buildout',
       'Development Status :: 3 - Alpha',
       'Intended Audience :: Developers',
       'License :: OSI Approved :: Zope Public License',
       'Topic :: Software Development :: Build Tools',
       'Topic :: Software Development :: Libraries :: Python Modules',
       ],
    )
