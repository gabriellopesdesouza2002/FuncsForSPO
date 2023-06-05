"""
    ## DIREITOS RESERVADOS / RIGHTS RESERVED / DERECHOS RESERVADOS

    ## https://online2pdf.com/pt/converter-pdf-para-txt-com-ocr

    Esse robô envia o PDF para o site https://online2pdf.com/pt/converter-pdf-para-txt-com-ocr
        e recupera um arquivo txt com o ocr
    
    Args:
        file_pdf (str): Caminho do arquivo
        dir_exit (str, optional): Local de saída do arquivo TXT. Defaults to `'output'`.
        get_text_into_code (bool, optional): Retorna o texto do pdf no código. Defaults to True.
        headless (bool, optional): executa como headless. Defaults to `True`.
        prints (bool, optional): Mostra o acompanhamento do OCR. Defaults to `True`.
        
    Use:
        >>> text = faz_ocr_em_pdf('MyPDF.pdf')
        >>> print(text)
        
    """

from FuncsForSPO.fpdf.focr.__ocr_online import GetTextPDF
from FuncsForSPO.fpython.functions_for_py import *
import requests
import json
import os
import base64

class ErroAPI(Exception):
    pass

def faz_ocr_em_pdf(file_pdf: str, dir_exit: str='output', get_text_into_code: bool=True, headless: bool=True, prints=False) -> str:
    """
    ## DIREITOS RESERVADOS / RIGHTS RESERVED / DERECHOS RESERVADOS

    ## https://online2pdf.com/pt/converter-pdf-para-txt-com-ocr

    Esse robô envia o PDF para o site https://online2pdf.com/pt/converter-pdf-para-txt-com-ocr
        e recupera um arquivo txt com o ocr
    
    Args:
        file_pdf (str): Caminho do arquivo
        dir_exit (str, optional): Local de saída do arquivo TXT. Defaults to `'output'`.
        get_text_into_code (bool, optional): Retorna o texto do pdf no código. Defaults to True.
        headless (bool, optional): executa como headless. Defaults to `True`.
        prints (bool, optional): Mostra o acompanhamento do OCR. Defaults to `True`.
        
    Use:
        >>> text = faz_ocr_em_pdf('MyPDF.pdf')
        >>> print(text)
        
    """
    
    bot = GetTextPDF(file_pdf=file_pdf, dir_exit=dir_exit, get_text_into_code=get_text_into_code, headless=headless, prints=prints)
    if get_text_into_code:
        return bot.recupera_texto()


def faz_ocr_em_pdf_offline(path_pdf: str, export_from_file_txt: str=False) -> str:
    """Converte pdf(s) em texto com pypdf
    
    ### pip install pypdf
    
    ## Atenção, só funciona corretamente em PDF's que o texto é selecionável!
    
    Use:
        ...
    
    Args:
        path_pdf (str): caminho do pdf
        export_from_file_txt (bool | str): passar um caminho de arquivo txt para o texto sair

    Returns:
        str: texto do PDF
    """
    
    text = []
    from pypdf import PdfReader

    reader = PdfReader(path_pdf)
    pages = reader.pages
    for page in pages:
        text.append(page.extract_text())
    else:
        text = transforma_lista_em_string(text)
        
        if export_from_file_txt:
            with open('extraction_pdf.txt', 'w', encoding='utf-8') as f:
                f.write(text)
        return text

def ocr_paycon(pdf_path, clear_task, user, password, sleep_for_request=5):
    auth = (user, password)
    
    # URL da rota de API
    url = 'https://gabrielpaycon.pythonanywhere.com/pdf/ocr-pdf-tesseract-send-file'

    # Arquivo PDF para enviar
    with open(pdf_path, 'rb') as file:
        print('fazendo base64')
        base64_pdf = base64.b64encode(file.read()).decode('utf-8')

        # Parâmetros da solicitação POST
        params = {'file': base64_pdf}
        data = json.dumps(params)

        # Faz a solicitação POST
        print('Enviando solicitação POST com o base64')
        try:
            response = requests.post(url, data=data, headers={'Content-Type': 'application/json'}, auth=auth)
        except Exception as e:
            print(e)
            ocr_paycon(pdf_path, user, password)
        print(response.json())
        # Exibe a resposta da API
        id_ = response.json().get('id')

        while True:
            # Define a URL da rota de API
            url = 'https://gabrielpaycon.pythonanywhere.com/verify-work-ocr'

            # Define o corpo da solicitação com o ID do trabalho de OCR
            if clear_task:
                params = {'id': id_, 'delete':'True'}
            else:
                params = {'id': id_, 'delete':'False'}
            data = json.dumps(params)
            # Envia a solicitação HTTP POST com o corpo JSON
            sleep(sleep_for_request)
            response = requests.post(url, data=data, headers={'Content-Type': 'application/json'})

            # Extrai o texto da resposta JSON
            try:
                response_json = response.json()
            except Exception as e:
                print(e)
                raise ErroAPI('ErroAPI')
            if response_json.get('status') == 'finalizado':
                return response_json.get('result')
            else:
                print(response_json.get('status'))
