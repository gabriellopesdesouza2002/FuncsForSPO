import os
from setuptools import setup

version = '6.7.0'


with open("README.md", "r", encoding='utf-8') as fh:
    readme = fh.read()
    setup(
        name='FuncsForSPO',
        version=version,
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
            os.path.join('FuncsForSPO', 'fgpt'),
            os.path.join('FuncsForSPO', 'flanguage'),
            os.path.join('FuncsForSPO', 'flanguage', 'translator'),
            os.path.join('FuncsForSPO', 'fopenpyxl'),
            os.path.join('FuncsForSPO', 'fpdf'),
            os.path.join('FuncsForSPO', 'fpdf', 'fanalyser'),
            os.path.join('FuncsForSPO', 'fpdf', 'fcompress'),
            os.path.join('FuncsForSPO', 'fpdf', 'fhtml_to_pdf'),
            os.path.join('FuncsForSPO', 'fpdf', 'fimgpdf'),
            os.path.join('FuncsForSPO', 'fpdf', 'focr'),
            os.path.join('FuncsForSPO', 'fpdf', 'pdfutils'),
            os.path.join('FuncsForSPO', 'fpysimplegui'),
            os.path.join('FuncsForSPO', 'fpython'),
            os.path.join('FuncsForSPO', 'fpython'),
            os.path.join('FuncsForSPO', 'fregex'),
            os.path.join('FuncsForSPO', 'fselenium'),
            os.path.join('FuncsForSPO', 'fsqlite'),
            os.path.join('FuncsForSPO', 'fwinotify'),
            os.path.join('FuncsForSPO', 'utils'),
        ],
        
        install_requires= [
            'selenium',
            'bs4',
            'requests',
            'html5lib',
            'openpyxl',
            'webdriver-manager',
            'pretty-html-table',
            'packaging',
            'PySimpleGUI',
            'macholib',
            'wget',
            'winotify',
            'pypdf',
            'pywin32',
            'gdown',
            'pytesseract',
            'xlsxwriter',
            'PyMuPDF',
            'PyPDF2',
            'pandas',
            'sqlalchemy',
            'rich',
            'pyinstaller==5.12.0',
        ],
        )
