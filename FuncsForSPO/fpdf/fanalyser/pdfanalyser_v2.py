from FuncsForSPO.fpdf.fanalyser.__pdfanalyser import *

def analyse_pdf_with_gpt(file_pdf:str, prompt:str, headless=True) -> str|dict:
    """
    DIREITOS RESERVADOS / RIGHTS RESERVED / DERECHOS RESERVADOS

    https://pdf.ai/

    Esse robô envia o PDF para o site e recupera o texto com a resposta do GPT
    
	This function analyses a PDF file using GPT (Generative Pre-trained Transformer) language model.
	
	:param file_pdf: A string representing the path to the PDF file.
	:param prompt: A string representing a prompt to start the analysis.
	:param credentials: A tuple containing the username and password.
	:param headless: A boolean indicating if the browser should run in headless mode. Default is True.
	:return: A string with the analysis result.
	"""
    # CREDENTIALS EXEMPLE -> (username, password)
    app = GPTPDFV2(file_pdf=file_pdf, prompt=prompt, headless=headless)
    text = app.run()
    return text

def analyse_pdf_with_gpt_v3(file_pdf:str, prompt:str, openai_key:str, headless=True) -> str:
    """
    DIREITOS RESERVADOS / RIGHTS RESERVED / DERECHOS RESERVADOS

    https://pdf.ai/

    Esse robô envia o PDF para o site e recupera o texto com a resposta do GPT
    
	This function analyses a PDF file using GPT (Generative Pre-trained Transformer) language model.
	
	:param file_pdf: A string representing the path to the PDF file.
	:param prompt: A string representing a prompt to start the analysis.
	:param credentials: A tuple containing the username and password.
	:param headless: A boolean indicating if the browser should run in headless mode. Default is True.
	:return: A string with the analysis result.
	"""
    # CREDENTIALS EXEMPLE -> (username, password)
    app = GPTPDFV3(file_pdf=file_pdf, prompt=prompt, openai_key=openai_key, headless=headless)
    text = app.run()
    return text


# file_pdf='initial_9232.pdf', prompt='analise e me fale em portugues esse pdf', headless=True, credentials=('githubpaycon', 'bolarede792')

