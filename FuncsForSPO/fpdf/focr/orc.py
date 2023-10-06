from FuncsForSPO.fpdf.focr.__ocr_online_v2 import OCRPDFV2
from FuncsForSPO.fpdf.focr.__ocr_online import GetTextPDF
from FuncsForSPO.fpython.functions_for_py import *
from FuncsForSPO.fpdf.pdfutils.pdfutils import split_pdf
from tqdm import tqdm
from PIL import Image
import fitz, uuid, os, gdown, pytesseract

def faz_ocr_em_pdf_offline(path_pdf: str, export_from_file_txt: str=False) -> str:
    """Converte pdf(s) em texto com pypdf
        
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

def ocr_tesseract(pdf, dpi=300, file_output=uuid.uuid4(), return_text=True, config_tesseract='', limit_pages=None, lang='por'):
    """Executa OCR em um arquivo PDF usando Tesseract e retorna o texto extraído ou o caminho para o arquivo de texto.

    Esta função realiza o OCR em um arquivo PDF usando Tesseract. Se necessário, ela baixará e extrairá os binários 
    do Tesseract. O PDF é convertido em imagens antes de realizar o OCR. O texto extraído é salvo em um arquivo, e 
    o conteúdo desse arquivo ou o seu caminho podem ser retornados.

    Use:
        >>> ocr_tesseract('meu_documento.pdf', dpi=300, return_text=True, lang='por')
        Retorna o texto extraído do arquivo 'meu_documento.pdf'.

    Args:
        pdf (str): O caminho para o arquivo PDF no qual o OCR será realizado.
        dpi (int, optional): A resolução DPI para converter páginas PDF em imagens. Padrão é 300.
        file_output (str, optional): O nome do arquivo de saída onde o texto OCR será salvo. Padrão é um UUID gerado.
        return_text (bool, optional): Se True, retorna o texto extraído; se False, retorna o caminho para o arquivo de texto. 
            Padrão é True.
        config_tesseract (str, optional): Configurações adicionais para o Tesseract. Padrão é uma string vazia.
        limit_pages (int, optional): Limita o número de páginas do PDF a serem processadas. Se None, todas as páginas serão processadas. 
            Padrão é None.
        lang (str, optional): O código de idioma usado pelo Tesseract para o OCR. Padrão é 'por' (português).

    Returns:
        str: Se `return_text` for True, retorna o texto extraído; se False, retorna o caminho para o arquivo de texto.

    Raises:
        Exception: Se ocorrer um erro durante o processamento, o OCR ou a escrita do arquivo.
    """
    path_exit = arquivo_com_caminho_absoluto('temp_tess', 'Tesseract-OCR.zip')
    path_tesseract_extract = arquivo_com_caminho_absoluto('bin', 'Tesseract-OCR')
    path_tesseract = arquivo_com_caminho_absoluto(('bin', 'Tesseract-OCR'), 'tesseract.exe')

    if not os.path.exists(path_tesseract):
        faz_log('Baixando binários do Tesseract, aguarde...')
        cria_dir_no_dir_de_trabalho_atual('temp_tess')
        cria_dir_no_dir_de_trabalho_atual('bin')
        gdown.download('https://drive.google.com/uc?id=1yX6I7906rzo3YHK5eTmdDOY4FulpQKJ-', path_exit, quiet=True)
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
                # Converte para escala de cinza
                gray = image.convert('L')

                # Aplica thresholding
                threshold = 128  # Ajuste conforme necessário
                binary = gray.point(lambda p: p > threshold and 255)

                binary.save(f'pages/{i}.png')
                bar.update(1)
        

        files = arquivos_com_caminho_absoluto_do_arquivo('pages')
        with tqdm(total=len(files), desc='OCR') as bar:
            for i, image in enumerate(files):
                text = pytesseract.image_to_string(image, config=config_tesseract, lang=lang)
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