from setuptools import setup, find_packages

setup(
    name='swpackage',
    version='1.0.0',
    description='a python project to interact with the Star Wars API',
    author='fajkoson',
    author_email='notsharing@sorryboys.com',
    url='https://github.com/fajkoson/swapi/',
    packages=find_packages(where='src'),  
    package_dir={'': 'src'},
    python_requires='>=3.12',  
    install_requires=[
        'aiohttp>=3.7.4',
        'PyYAML>=6.0.1',
        'aiofiles>=23.2.1',    
    ],
    extras_require={
        'dev': [
            'pytest>=6.2.2', 
            'pytest-asyncio>=0.14.0',
            'mypy>=1.9.0',
            'pytest>=8.1.1',
            'pytest-mock>=3.12.0',
            'types-aiofiles>=23.2.0.20240311',
            'types-PyYAML>=6.0.12.20240311',
        ],
    }, 
    
    entry_points={
        'console_scripts': [
            'swpackage=swpackage.sw_world:run_main',
            'tests=tests.run_tests:run_main',            
        ],
    },
    include_package_data=True,  
    
)
