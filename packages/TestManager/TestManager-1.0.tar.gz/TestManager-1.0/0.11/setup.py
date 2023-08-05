from setuptools import setup

setup(
    name='TestManager',
    version='1.0',
    packages=['testmanager'],
    package_data={'testmanager' : ['*.txt', 'templates/*.html', 'htdocs/js/*.js', 'htdocs/css/*.css', 'htdocs/images/*.*']},
    author = 'Roberto Longobardi, Marco Cipriani',
    license='BSD',
    url='http://trac-hacks.org/wiki/TestManagerForTracPlugin',
    description='Test management plugin for Trac',
    entry_points = {'trac.plugins': ['testmanager = testmanager']},
    dependency_links=['http://svn.edgewall.org/repos/genshi/trunk#egg=Genshi-dev'],
    install_requires=['Genshi >= 0.5'],
    )
