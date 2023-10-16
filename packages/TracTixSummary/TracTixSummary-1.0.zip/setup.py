from setuptools import find_packages, setup

setup(
    name='TracTixSummary', version='1.0',
    packages=find_packages(exclude=['*.tests*']),
    entry_points = {
        'trac.plugins': [
            'helloworld = helloworld',
        ],
    },
    package_data = {
        'helloworld': [
            'templates/*.html', 
            'htdocs/css/*.css', 
            'htdocs/images/*'
        ]
    },
	zip_safe=False,
)

