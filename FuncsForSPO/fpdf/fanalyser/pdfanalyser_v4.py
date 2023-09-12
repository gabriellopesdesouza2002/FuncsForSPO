from FuncsForSPO.fpdf.fanalyser.__pdfanalyser import *

def analyse_pdf_with_gpt(file_pdf:str, prompt:str, timeout=180, headless=True) -> str:
    """
    DIREITOS RESERVADOS / RIGHTS RESERVED / DERECHOS RESERVADOS

    https://www.chatpdf.com/

	"""
    # CREDENTIALS EXEMPLE -> (username, password)
    app = GPTPDFV3(file_pdf=file_pdf, prompt=prompt, timeout=timeout, headless=headless)
    text = app.run()
    return text.replace('Olá, eu sou uma assistente de documentos multilíngue e estou aqui para ajudá-lo com qualquer dúvida que você possa ter sobre o documento que você enviou. ', '')
