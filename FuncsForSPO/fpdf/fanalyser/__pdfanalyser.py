"""
DIREITOS RESERVADOS / RIGHTS RESERVED / DERECHOS RESERVADOS

https://pdf.ai/

Esse robô envia o PDF para o site https://pdf.ai/
    e recupera um arquivo txt com a resposta do GPT
"""
from FuncsForSPO.fpdf.fanalyser.base import *

class ErroPDFAIException(Exception):
    pass

class GPTPDF(BotMain):    
    def __init__(self, file_pdf: str, credentials:tuple, prompt:str, headless: bool=True) -> str:
        self.PDF_PATH = os.path.abspath(file_pdf)
        self.PROMPT = prompt
        self.HEADLESS = headless
        self.CREDENTIALS = credentials
        super().__init__(self.HEADLESS)
    
    def run(self):
        try:
            self.DRIVER.get('https://pdf.ai/auth/sign-in')
            espera_elemento_disponivel_e_clica(self.WDW, (By.CSS_SELECTOR, 'img[alt="Github logo"]~span'))
            espera_input_limpa_e_envia_send_keys(self.WDW, self.CREDENTIALS[0], (By.CSS_SELECTOR, '#login_field'))
            espera_input_limpa_e_envia_send_keys(self.WDW, self.CREDENTIALS[1]+'\n', (By.CSS_SELECTOR, '#password'))
            
            try:
                espera_elemento_disponivel_e_clica(self.WDW, (By.CSS_SELECTOR, 'button[data-octo-click="oauth_application_authorization"]'))
            except (NoSuchElementException, TimeoutException):
                pass
            

            while True:
                try:
                    faz_log('Limpando documentos anteriores')
                    elements = espera_e_retorna_lista_de_elementos(self.WDW3, (By.CSS_SELECTOR, 'tbody>tr>td:last-child>button'))
                    for i in elements:
                        i.click()
                        espera_elemento_disponivel_e_clica(self.WDW, (By.CSS_SELECTOR, 'h3~div>button'))
                        espera_elemento_sair_do_dom(self.WDW, (By.CSS_SELECTOR, 'h3~div>button'))
                        break
                except (NoSuchElementException, TimeoutException):
                    break


            espera_elemento_disponivel_e_clica(self.WDW10, (By.CSS_SELECTOR, 'button:last-of-type span'))
            espera_elemento(self.WDW, (By.CSS_SELECTOR, 'input[type="file"]'), in_dom=True)
            self.DRIVER.find_element(By.CSS_SELECTOR, 'input[type="file"]').send_keys(self.PDF_PATH)
            espera_elemento_disponivel_e_clica(self.WDW, (By.CSS_SELECTOR, 'div[class*="flex justify-between"]>button'))


            while True:
                try:
                    espera_input_limpa_e_envia_send_keys(self.WDW30, 'Coloque no inicio da sua resposta: "IA" e me responda em português. '+self.PROMPT, (By.CSS_SELECTOR, 'textarea[placeholder*="Send"]'))
                    espera_elemento_disponivel_e_clica(self.WDW30, (By.CSS_SELECTOR, 'textarea[placeholder*="Send"]~button'))
                    break
                except ElementClickInterceptedException:
                    try:
                        self.DRIVER.execute_script("arguments[0].remove();", self.DRIVER.find_element(By.CSS_SELECTOR, '#__NEXT_DATA__~ins'))
                    except Exception:
                        pass

            while True:
                faz_log('Aguardando resposta...')
                text = espera_e_retorna_elemento_text(self.WDW, (By.CSS_SELECTOR, '#__next main>div~div>div~div>div>div>div>div~div'))
                if 'IA' in text:
                    break
                else:
                    sleep(2)
                    continue
            self.DRIVER.get('https://pdf.ai/documents')
            espera_elemento_disponivel_e_clica(self.WDW, (By.CSS_SELECTOR, 'a[href="/auth/account"]~button'))
            sleep(2)
            self.DRIVER.quit()
            return text
        except Exception as e:
            faz_log(repr(e), 'c*')
            faz_log(self.DRIVER.get_screenshot_as_base64(), 'i*')
            self.DRIVER.quit()
            raise ErroPDFAIException
