from FuncsForSPO.fpdf.fanalyser.pdfanalyser_v3 import *
from FuncsForSPO.fpdf.focr.orc import ocr_tesseract

def test_analyse_pdf_with_gpt():
    text = ocr_tesseract('initial_9257_15.pdf', 600)
    print(analyse_pdf_with_gpt(text, 'Se for de fato uma petição inicial, analise todo o conteúdo da petição, desde a introdução até os pedidos finais; Identifique o tema principal e identifique o assunto e o sub-assunto da petição inicial gostaria também que você colocasse os pedidos em tópicos, separando uma infomração da outra'))

def test_translate_open():
    import requests
    import json

    url = "https://libretranslate.com/translate"
    data = {
        "q": "Ciao!",
        "source": "auto",
        "target": "en"
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(response.json())
    
test_translate_open()