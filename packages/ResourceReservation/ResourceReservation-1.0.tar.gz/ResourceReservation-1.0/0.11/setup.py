from setuptools import setup

setup(
    name='ResourceReservation',
    version='1.0',
    packages=['resreservation'],
    package_data={'resreservation' : ['*.txt', 'templates/*.html', 'htdocs/js/*.js', 'htdocs/css/*.css', 'htdocs/images/*.*']},
    author = 'Roberto Longobardi',
    license='BSD',
    url='http://trac-hacks.org/wiki/ResourceReservationPlugin',
    description='Resource Reservation plugin for Trac',
    entry_points = {'trac.plugins': ['resreservation = resreservation']},
    dependency_links=['http://svn.edgewall.org/repos/genshi/trunk#egg=Genshi-dev'],
    install_requires=['Genshi >= 0.5'],
    )
