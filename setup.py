import os
from setuptools import setup

version = '6.3.2'

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
            'selenium==4.10.0',
            'bs4==0.0.1',
            'requests==2.31.0',
            'html5lib==1.1',
            'openpyxl==3.1.2',
            'webdriver-manager==3.8.6',
            'pretty-html-table==0.9.16',
            'packaging==23.1',
            'PySimpleGUI==4.60.5',
            'macholib==1.16.2',
            'wget==3.2',
            'winotify==1.1.0',
            'pypdf==3.11.0',
            'pywin32==306',
            'gdown==4.7.1',
            'pytesseract==0.3.10',
            'PyMuPDF==1.22.5',
            'PyPDF2==3.0.1',
            'sqlalchemy==2.0.17',
            'rich==12.6.0',
            'pyinstaller==5.6.2',
        ],
        )
