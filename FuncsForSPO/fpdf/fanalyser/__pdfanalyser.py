"""
DIREITOS RESERVADOS / RIGHTS RESERVED / DERECHOS RESERVADOS

https://pdf.ai/

Esse robô envia o PDF para o site https://pdf.ai/
    e recupera um arquivo txt com a resposta do GPT
"""
from FuncsForSPO.fpdf.fanalyser.base import *

class ErroPDFAIException(Exception):
    pass

class GPTPDFV1(BotMain):    
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
            espera_elemento_disponivel_e_clica(self.WDW330, (By.CSS_SELECTOR, 'div[class*="flex justify-between"]>button'))


            while True:
                try:
                    espera_input_limpa_e_envia_send_keys(self.WDW330, 'é de suma importância que você coloque no inicio da sua resposta: "IA" e me responda em português. '+self.PROMPT, (By.CSS_SELECTOR, 'textarea[placeholder*="Send"]'))
                    espera_elemento_disponivel_e_clica(self.WDW330, (By.CSS_SELECTOR, 'textarea[placeholder*="Send"]~button'))
                    break
                except ElementClickInterceptedException:
                    try:
                        self.DRIVER.execute_script("arguments[0].remove();", self.DRIVER.find_element(By.CSS_SELECTOR, '#__NEXT_DATA__~ins'))
                    except Exception:
                        pass
            
            tentativas = 20
            text = ''
            while tentativas > 0:
                faz_log('Aguardando resposta...')
                text = espera_e_retorna_elemento_text(self.WDW, (By.CSS_SELECTOR, '#__next main>div~div>div~div>div>div>div>div~div'))
                if 'IA' in text or 'sorry' in text.lower() or tentativas == 1:
                    break
                else:
                    faz_log(f'Resposta até agora: "{text}"')
                    tentativas -= 1
                    sleep(5)
                    continue
            self.DRIVER.get('https://pdf.ai/documents')
            espera_elemento_disponivel_e_clica(self.WDW, (By.CSS_SELECTOR, 'a[href="/auth/account"]~button'))

            self.DRIVER.get('https://github.com/settings/sessions')
            self.DRIVER.get('https://github.com/settings/sessions')
            self.DRIVER.get('https://github.com/settings/sessions')
            sessions = espera_e_retorna_conteudo_dos_atributos_dos_elementos_text(self.WDW, 'href', (By.CSS_SELECTOR, 'a[href*="/settings/sessions/"]'))
            for session in sessions:
                self.DRIVER.get(session)
                try:
                    espera_elemento_disponivel_e_clica(self.WDW, (By.CSS_SELECTOR, '#settings-frame div > form > button'))
                except (NoSuchElementException, TimeoutException):
                    pass
            sleep(2)
            self.DRIVER.quit()
            if tentativas == 0:
                raise ErroPDFAIException('Muitas tentativas, tente uma nova solicitação')
            return text
        except Exception as e:
            faz_log(repr(e), 'c*')
            faz_log(self.DRIVER.get_screenshot_as_base64(), 'i*')
            self.DRIVER.quit()
            raise ErroPDFAIException

class GPTPDFV2(BotMain):    
    def __init__(self, content_txt: str, prompt:str, headless: bool=True) -> str:
        cria_dir_no_dir_de_trabalho_atual('tempdir')
        faz_log('Criando arquivo em uma pasta temporária')
        self.TXT_CONTENT = arquivo_com_caminho_absoluto('tempdir', 'temp.txt')
        with open(self.TXT_CONTENT, 'w', encoding='utf-8') as f:
            f.write(content_txt)
        
        
        self.PROMPT = prompt
        self.HEADLESS = headless
        super().__init__(self.HEADLESS)
    
    def run(self):
        try:
            faz_log('Indo para askyourpdf')
            self.DRIVER.get('https://askyourpdf.com/')
            espera_elemento(self.WDW, (By.CSS_SELECTOR, 'input[type="file"]'), in_dom=True)
            self.DRIVER.find_element(By.CSS_SELECTOR, 'input[type="file"]').send_keys(self.TXT_CONTENT)
            
            faz_log('Documento enviado, aguardando entrada para o prompt')
            espera_input_limpa_e_envia_send_keys(self.WDW130, 'Adicione "AI RESPONSE" apenas no final da sua resposta (isso é de suma importância) e deve ser tudo em português! '+self.PROMPT, (By.CSS_SELECTOR, 'textarea[placeholder="Write your question"]'))
            espera_elemento_disponivel_e_clica(self.WDW130, (By.CSS_SELECTOR, 'button[class*="ant-btn-default"]'))
            faz_log('Esperando a resposta')
            start_time = time.time()
            timeout = 180  # Tempo limite em segundos

            while True:
                try:
                    text = espera_e_retorna_elemento_text(self.WDW, (By.CSS_SELECTOR, 'div[style="padding: 5px;"]>div:last-of-type>div:last-of-type span'))
                    faz_log(f'Resposta até agora: [green]{text}[/green]')
                    time.sleep(7)
                except:
                    # Lidar com exceções, se necessário
                    pass

                if 'AI RES' in text:
                    break
                if 'try again.' in text.lower():
                    text = text + '  Não foi possível ter uma interpretação adequada. Tente outro prompt'
                    break

                elapsed_time = time.time() - start_time
                if elapsed_time >= timeout:
                    # Tempo limite atingido, interromper o loop
                    break
            faz_log('Recuperando o id do documento')
            self.apaga_arquivo_da_base_do_site()
            self.DRIVER.close()
            return text
        except Exception as e:
            faz_log(repr(e), 'c*')
            faz_log(self.DRIVER.get_screenshot_as_base64(), 'i*')
            self.DRIVER.quit()
            raise ErroPDFAIException
        
    def apaga_arquivo_da_base_do_site(self):
        url = self.DRIVER.current_url
        id_ = re.sub(r'.*?/chat/', '', url)
        self.DRIVER.get('https://askyourpdf.com/delete')
        espera_elemento_e_envia_send_keys(self.WDW, id_, (By.CSS_SELECTOR, 'input'))
        espera_elemento_disponivel_e_clica(self.WDW, (By.CSS_SELECTOR, 'button'))
        sleep(2)
        faz_log('Documento deletado da base de dados!')
        os.remove(self.TXT_CONTENT)