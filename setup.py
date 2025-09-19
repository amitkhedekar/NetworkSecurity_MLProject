'''
The setup.py file is an essential part of packaging and distributing Python projects. 
It is used by setuptools (or distutils in older python versions) to define the configuration
of your projects, such as its metadata, dependencies and more
'''

from setuptools import find_packages, setup
from typing import List

def get_requirements()->List[str]:
    '''
    This function will return list of requirements
    '''
    
    HYPEN_E_DOT = '-e .'
    requirement_lst=[]
    try:
        with open('requirements.txt' , 'r') as file:
            #read lines from file
            lines = file.readlines()

            #process each line
            for line in lines:
                requirement = line.split()

                #ignore empty line and -e .
                if requirement and HYPEN_E_DOT in requirement:
                    requirement_lst.append(requirement)
                 
    except FileNotFoundError:
        print('requirements.txt file not found.')
    
    return requirement_lst

setup(
    name             = 'Network Security',
    version          = '0.0.1',
    author           = 'Amit',
    author_email     = 'amit.khedekar9@gmail.com',
    packages         = find_packages(),
    install_requires = get_requirements(), 
)