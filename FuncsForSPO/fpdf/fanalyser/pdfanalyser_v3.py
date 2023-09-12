from FuncsForSPO.fpdf.fanalyser.__pdfanalyser import *

def analyse_pdf_with_gpt(content_txt:str, prompt:str|dict, headless=True) -> str:
    """
    DIREITOS RESERVADOS / RIGHTS RESERVED / DERECHOS RESERVADOS

    https://askyourpdf.com/
    
	Takes in a string of PDF content, a prompt for the GPT model, and a boolean flag indicating whether to run the 
	model in headless mode or not. Returns a string with the result of running the GPT model on the provided PDF 
	content. The returned string is the same as the model result, with a specific greeting string removed.
	
	:param content_txt: A string of PDF content to be analyzed
	:type content_txt: str
	
	:param prompt: A string prompt for the GPT model
	:type prompt: str
	
	:param headless: A boolean flag indicating whether to run the GPT model in headless mode or not (default is True)
	:type headless: bool
	
	:return: A string with the result of running the GPT model on the provided PDF content
	:rtype: str
	"""
    # CREDENTIALS EXEMPLE -> (username, password)
    app = GPTPDFV2(content_txt=content_txt, prompt=prompt, headless=headless)
    text = app.run()
    return text


