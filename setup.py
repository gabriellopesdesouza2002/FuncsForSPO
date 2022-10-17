from setuptools import setup

with open("README.md", "r", encoding='utf-8') as fh:
    readme = fh.read()

setup(
    name='FuncsForSPO',
    version='0.0.4.9.6',
    url='https://github.com/githubpaycon/FuncsForSPO',
    license='MIT License',
    author='Gabriel Lopes de Souza',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='githubpaycon@gmail.com',
    keywords='Funções Para Melhorar Desenvolvimento de Robôs com Selenium',
    description=u'Funções Para Melhorar Desenvolvimento de Robôs com Selenium',
    packages=[
        'FuncsForSPO',
        'FuncsForSPO\\fftp',
        'FuncsForSPO\\fexceptions',
        'FuncsForSPO\\fopenpyxl',
        'FuncsForSPO\\fpysimplegui',
        'FuncsForSPO\\fpython',
        'FuncsForSPO\\focr',
        'FuncsForSPO\\fregex',
        'FuncsForSPO\\fselenium',
        'FuncsForSPO\\fselenium',
        'FuncsForSPO\\fwinotify',
        'FuncsForSPO\\femails',
        'FuncsForSPO\\fsqlite'
        ],
    install_requires=[
        'selenium', 
        'openpyxl', 
        'webdriver-manager', 
        'fake_useragent', 
        'requests',
        'pretty_html_table',
        'pywin32',
        'PySimpleGUI',
        'PyInstaller',
        'pywin32-ctypes',
        'macholib',
        'wget',
        'winotify'
        ],
    )