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

from FuncsForSPO.fpdf.focr.__ocr_online_v2 import OCRPDFV2
from FuncsForSPO.fpdf.focr.__ocr_online import GetTextPDF
from FuncsForSPO.fpython.functions_for_py import *
from FuncsForSPO.fpdf.pdfutils.pdfutils import split_pdf
import requests
import json
import os
import base64
from tqdm import tqdm
import gdown
import pytesseract
from PIL import Image
import fitz
import uuid

class ErroAPI(Exception):
    pass

def faz_ocr_em_pdf(file_pdf: str, type_extract='text', dir_exit: str='output', get_text_into_code: bool=True, headless: bool=True, prints=False) -> str:
    """
    ## DIREITOS RESERVADOS / RIGHTS RESERVED / DERECHOS RESERVADOS

    ## https://online2pdf.com/pt/converter-pdf-para-txt-com-ocr

    Esse robô envia o PDF para o site https://online2pdf.com/pt/converter-pdf-para-txt-com-ocr
        e recupera um arquivo txt com o ocr
    
    Args:
        file_pdf (str): Caminho do arquivo
        dir_exit (str, optional): Local de saída do arquivo TXT. Defaults to `'output'`.
        headless (bool, optional): executa como headless. Defaults to `True`.
        prints (bool, optional): Mostra o acompanhamento do OCR. Defaults to `True`.
        
    Use:
        >>> text = faz_ocr_em_pdf('MyPDF.pdf')
        >>> print(text)

    """
    files = split_pdf(file_pdf)
    if len(files) > 1:
        faz_log(f'Serão processados {len(files)} PDF(s) no total | (São mais de 30 páginas no PDF)')
        text_all = ''
        with tqdm(total=len(files), desc="Progresso", unit="PDF") as pbar:
            for i, file_ in enumerate(files):
                # faz_log(f'Fazendo OCR do PDF {i+1} de {len(files)}: {os.path.basename(file_)}')
                bot = GetTextPDF(file_pdf=file_, dir_exit=dir_exit, headless=headless, prints=prints)
                text_all += bot.recupera_texto()
                pbar.update(1)
            else:
                return text_all
    else:
        bot = GetTextPDF(file_pdf=file_pdf, dir_exit=dir_exit, headless=headless, prints=prints)
        return bot.recupera_texto()


def faz_ocr_em_pdf_v2(file_pdf: str, headless: bool=True) -> str:
    bot = OCRPDFV2(file_pdf=file_pdf, headless=headless)
    bot.run()


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


def ocr_tesseract(pdf, dpi=300, file_output=uuid.uuid4(), return_text=True, config_tesseract='', limit_pages=None):
    """
    Perform optical character recognition (OCR) on a PDF using Tesseract.

    Args:
        pdf (str): The path to the input PDF file.
        dpi (int, optional): The resolution in dots per inch (DPI) for the OCR process. Defaults to 300.
        file_output (str, optional): The output file name for the OCR result. Defaults to a randomly generated UUID.
        return_text (bool, optional): Specifies whether to return the OCR result as a string directly in the code or as the path to the output file. Defaults to True.
        config_tesseract (str, optional): Additional configuration options for Tesseract. Defaults to an empty string.
        limit_pages (int, optional): Maximum number of pages to process. If None, all pages are processed. Defaults to None.

    Returns:
        str: The OCR result as a string if `return_text` is True, otherwise the path to the output file.
    """

    # se for return_text, retornará o texto no diretamente no código, se for false, retornará o caminho do arquivo com a resposta do OCR

    path_exit = arquivo_com_caminho_absoluto('temp_tess', 'Tesseract-OCR.zip')
    path_tesseract_extract = arquivo_com_caminho_absoluto('bin', 'Tesseract-OCR')
    path_tesseract = arquivo_com_caminho_absoluto(('bin', 'Tesseract-OCR'), 'tesseract.exe')

    if not os.path.exists(path_tesseract):
        faz_log('Baixando binários do Tesseract, aguarde...')
        cria_dir_no_dir_de_trabalho_atual('temp_tess')
        cria_dir_no_dir_de_trabalho_atual('bin')
        gdown.download('https://drive.google.com/uc?id=1yK0BwNuvEHhX1Nb2HjTP0ZaZvlhktpYR', path_exit, quiet=True)
        sleep(1)
        with zipfile.ZipFile(path_exit, 'r') as zip_ref:
            # Obtém o nome da pasta interna dentro do arquivo ZIP
            zip_info = zip_ref.infolist()[0]
            folder_name = zip_info.filename.split("/")[0]

            # Extrai o conteúdo da pasta interna para a pasta de destino
            for file_info in zip_ref.infolist():
                if file_info.filename.startswith(f"{folder_name}/"):
                    file_info.filename = file_info.filename.replace(f"{folder_name}/", "", 1)
                    zip_ref.extract(file_info, path_tesseract_extract)
        deleta_diretorio('temp_tess')
    pytesseract.pytesseract.tesseract_cmd = path_tesseract

    with fitz.open(pdf) as pdf_fitz:
        cria_dir_no_dir_de_trabalho_atual('pages')
        limpa_diretorio('pages')
        faz_log(f'Convertendo PDF para páginas...')
        number_of_pages = len(pdf_fitz) if limit_pages is None else min(limit_pages, len(pdf_fitz))
        with tqdm(total=number_of_pages, desc='EXTRACT PAGES') as bar:
            for i, page in enumerate(pdf_fitz):
                if i >= number_of_pages:
                    break
                page = pdf_fitz.load_page(i)
                mat = fitz.Matrix(dpi/72, dpi/72)  # Matriz de transformação usando DPI
                pix = page.get_pixmap(matrix=mat)
                image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                image.save(f'pages/{i}.png')
                bar.update(1)
        

        files = arquivos_com_caminho_absoluto_do_arquivo('pages')
        with tqdm(total=len(files), desc='OCR') as bar:
            for i, image in enumerate(files):
                text = pytesseract.image_to_string(image, config=config_tesseract)
                with open(arquivo_com_caminho_absoluto('tempdir', f'{file_output}.txt'), 'a', encoding='utf-8') as f:
                    f.write(text)
                bar.update(1)
            else:
                limpa_diretorio('pages')
                if return_text:
                    text_all = ''
                    with open(arquivo_com_caminho_absoluto('tempdir', f'{file_output}.txt'), 'r', encoding='utf-8') as f:
                        text_all = f.read()
                    os.remove(arquivo_com_caminho_absoluto('tempdir', f'{file_output}.txt'))
                    return text_all
                else:
                    return os.path.abspath(arquivo_com_caminho_absoluto('tempdir', f'{file_output}.txt'))