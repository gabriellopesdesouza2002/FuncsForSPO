from FuncsForSPO.fselenium.functions_selenium import *
from FuncsForSPO.fpdf.fanalyser.pdfanalyser import *
# from FuncsForSPO.fgpt.pdfanalyser.__pdfanalyser import *
print(analyse_pdf_with_gpt('GatewayPDF.pdf', 'Por favor, verifique se é uma inicial, se for, diga-me os pedidos em tópicos se possível (exemplo: 1. pedido1; 2. pedido2), e se não for, diga-me que documento é detalhadamente.', credentials=('githubpaycon', 'bolarede792'), headless=True))
# app = GPTPDF(file_pdf='initial_9232.pdf', prompt='analise e me fale em portugues esse pdf', headless=True, credentials=('githubpaycon', 'bolarede792'))
# # app = GPTPDF('pdf_html.pdf', 'analise e me fale em portugues esse pdf', headless=False, credentials=('githubpaycon', 'bolarede792'))
# text = app.run()
# print(text)
# print(verifica_se_baixou_o_arquivo('base', '.txt', timeout=10, return_file=True))