import os
from setuptools import setup

with open("README.md", "r", encoding='utf-8') as fh:
    readme = fh.read()
    
    setup(
        name='FuncsForSPO',
        version='0.0.4.14',
        url='https://github.com/githubpaycon/FuncsForSPO',
        license='MIT License',
        author='Gabriel Lopes de Souza',
        long_description=readme,
        long_description_content_type="text/markdown",
        author_email='githubpaycon@gmail.com',
        keywords='Funções Para Melhorar Desenvolvimento de Robôs com Selenium',
        description=u'Funções Para Melhorar Desenvolvimento de Robôs com Selenium',
        
        packages= [
            os.path.join('FuncsForSPO', 'femails'),
            os.path.join('FuncsForSPO', 'fexceptions'),
            os.path.join('FuncsForSPO', 'fftp'),
            os.path.join('FuncsForSPO', 'fpdf'),
            os.path.join('FuncsForSPO', 'fpdf', 'focr'),
            os.path.join('FuncsForSPO', 'fpdf', 'fcompress'),
            os.path.join('FuncsForSPO', 'fopenpyxl'),
            os.path.join('FuncsForSPO', 'fpysimplegui'),
            os.path.join('FuncsForSPO', 'fpython'),
            os.path.join('FuncsForSPO', 'fpython'),
            os.path.join('FuncsForSPO', 'fregex'),
            os.path.join('FuncsForSPO', 'fselenium'),
            os.path.join('FuncsForSPO', 'fsqlite'),
            os.path.join('FuncsForSPO', 'fwinotify'),
        ],
        
        install_requires= [
            'selenium',
            'bs4',
            'requests',
            'html5lib',
            'openpyxl',
            'webdriver-manager',
            'fake_useragent',
            'requests',
            'pretty_html_table',
            'pywin32',
            'packaging',
            'PySimpleGUI',
            'PyInstaller',
            'pywin32-ctypes',
            'macholib',
            'wget',
            'winotify'
        ],
        )
