from setuptools import setup

setup(
    name='tornado-cli',
    version='0.1',    
    author='Stuart Marsh',
    author_email='stuart@beardygeek.com',
    packages=['tornado_cli','tornado_cli.commands', 'tornado_cli.project_template', 'tornado_cli.project_template.handlers', 'tornado_cli.project_template.logconfig',
                'tornado_cli.project_template.tests'],
    package_data={'tornado_cli.project_template':['media/.empty','templates/welcome.html']},                 
    license='MIT',           
    description='A command line interface helper for Tornado',
    entry_points=dict(console_scripts=['tcli=tornado_cli:main','tornado_cli=tornado_cli:main'])
)

