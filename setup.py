from setuptools import setup, find_packages

setup(
    name='swapi_fajkoson',
    version='0.1.0',
    description='a python project to interact with the Star Wars API',
    author='fajkoson',
    author_email='notsharing@sorryboys.com',
    packages=find_packages(where='src'),  
    package_dir={'': 'src'},  
    install_requires=[
        'requests',
        'aiohttp',
        'PyYAML',
        
    ],
    python_requires='>=3.6',  
    
    entry_points={
        'console_scripts': [
            'swapi_fajkoson=swapi_fajkoson.sw_world:main',
            
        ],
    },
    include_package_data=True,  
    
)
