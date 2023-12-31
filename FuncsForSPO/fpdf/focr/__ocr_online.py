"""
DIREITOS RESERVADOS / RIGHTS RESERVED / DERECHOS RESERVADOS

https://online2pdf.com/pt/converter-pdf-para-txt-com-ocr

Esse robô envia o PDF para o site https://online2pdf.com/pt/converter-pdf-para-txt-com-ocr
    e recupera um arquivo txt com o ocr
    

"""
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import *
from webdriver_manager.chrome import ChromeDriverManager
from FuncsForSPO.fpython.functions_for_py import *
from FuncsForSPO.fselenium.functions_selenium import *
from FuncsForSPO.fexceptions.exceptions import FalhaAoRecuperarOcr
import json
import os

class GetTextPDF:    
    def __init__(self, file_pdf: str, dir_exit: str='output', headless: bool=True, prints: bool=False, create_driver: bool=True) -> str:
        """Init

        Args:
            file_pdf (str): Caminho do arquivo
            dir_exit (str, optional): Local de saída do arquivo TXT. Defaults to 'output'.
            headless (bool, optional): executa como headless. Defaults to True.
            create_driver (bool, optional): Cria um driver. Defaults to True.
        """
        if isinstance(headless, (bool, int)):
            self.HEADLESS = headless
        else:
            print('Adicione True ou False para Headless')
        
        if isinstance(file_pdf, str):
            self.FILE_PDF = os.path.abspath(file_pdf)
            self.CONVERTER_VARIOS_ARQUIVOS = False
            self.MESCLAR_EM_UMA_LINHA = False
        else:
            print('Envie, uma string como caminho do parâmetro file_pdf')
            
        # --- CHROME OPTIONS --- #
        self._options = ChromeOptions()
        
        # --- PATH BASE DIR --- #        
        self.DOWNLOAD_DIR = cria_dir_no_dir_de_trabalho_atual('tempdir')
        limpa_diretorio('tempdir')
            
        self._SETTINGS_SAVE_AS_PDF = {
                    "recentDestinations": [
                        {
                            "id": "Save as PDF",
                            "origin": "local",
                            "account": ""
                        }
                    ],
                    "selectedDestinationId": "Save as PDF",
                    "version": 2,
                }


        self._PROFILE = {'printing.print_preview_sticky_settings.appState': json.dumps(self._SETTINGS_SAVE_AS_PDF),
                "savefile.default_directory":  f"{self.DOWNLOAD_DIR}",
                "download.default_directory":  f"{self.DOWNLOAD_DIR}",
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True}
            
        self._options.add_experimental_option('prefs', self._PROFILE)
        
        self._options.add_experimental_option("excludeSwitches", ["enable-logging"])
        if self.HEADLESS:
            self._options.add_argument('--headless')
            
        self._options.add_argument("--disable-web-security")
        self._options.add_argument("--allow-running-insecure-content")
        self._options.add_argument("--disable-extensions")
        self._options.add_argument("--start-maximized")
        self._options.add_argument("--no-sandbox")
        self._options.add_argument("--disable-setuid-sandbox")
        self._options.add_argument("--disable-infobars")
        self._options.add_argument("--disable-webgl")
        self._options.add_argument("--disable-popup-blocking")
        self._options.add_argument('--disable-gpu')
        self._options.add_argument('--disable-software-rasterizer')
        self._options.add_argument('--no-proxy-server')
        self._options.add_argument("--proxy-server='direct://'")
        self._options.add_argument('--proxy-bypass-list=*')
        self._options.add_argument('--disable-dev-shm-usage')
        self._options.add_argument('--block-new-web-contents')
        self._options.add_argument('--incognito')
        self._options.add_argument('–disable-notifications')
        self._options.add_argument('--suppress-message-center-popups')
        
        if create_driver:
            self.__service = Service(executable_path=ChromeDriverManager().install())
            self.DRIVER = Chrome(service=self.__service, options=self._options)
        else:
            self.DRIVER = Chrome(options=self._options)

        def enable_download_in_headless_chrome(driver, download_dir):
            """
            Esse código adiciona suporte ao navegador Chrome sem interface gráfica (headless) no Selenium WebDriver para permitir o download automático de arquivos em um diretório especificado.

            Mais especificamente, o código adiciona um comando ausente "send_command" ao executor de comando do driver e, em seguida, executa um comando "Page.setDownloadBehavior" para permitir o download automático de arquivos no diretório especificado.

            O primeiro passo é necessário porque o suporte para o comando "send_command" não está incluído no Selenium WebDriver por padrão. O segundo passo usa o comando "Page.setDownloadBehavior" do Chrome DevTools Protocol para permitir o download automático de arquivos em um diretório especificado.

            Em resumo, o código adiciona suporte para o download automático de arquivos em um diretório especificado no Chrome sem interface gráfica usando o Selenium WebDriver.
            """
            driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

            params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
            command_result = driver.execute("send_command", params)
        enable_download_in_headless_chrome(self.DRIVER, self.DOWNLOAD_DIR)

        # - WebDriverWaits - #
        self.WDW = WebDriverWait(self.DRIVER, timeout=3)
        self.WDW3 = WebDriverWait(self.DRIVER, timeout=3)
        self.WDW30 = WebDriverWait(self.DRIVER, timeout=30)
        self.WDW60 = WebDriverWait(self.DRIVER, timeout=60)
        self.WDW180 = WebDriverWait(self.DRIVER, timeout=180)
        self.DRIVER.maximize_window()
    
    # ----------------------------------------------------------------- #
        try:
            if prints:
                print('Acessando o site...')
            self.DRIVER.get('https://online2pdf.com/pt/converter-pdf-para-txt-com-ocr')
            
            if prints:
                print('Convertendo arquivo...')

            # Espera pelo elemento de enviar o arquivo
            self.WDW3.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#input_file0')))

            # Envia o arquivo
            self.DRIVER.find_element(By.CSS_SELECTOR, '#input_file0').send_keys(self.FILE_PDF)

            # Clica em OCR Profundo
            try:
                espera_elemento_disponivel_e_clica(self.WDW3, (By.CSS_SELECTOR, '#export_fullocr_box > label'))
            except (TimeoutException, NoSuchElementException):
                pass

            # Clica em Converter
            espera_elemento_disponivel_e_clica(self.WDW3, (By.CSS_SELECTOR, 'button[class="convert_button"]'))

            if prints:
                print('Carregando, por favor espere, essa parte deve demorar um pouco...')
            
            # espera o elemento de completo
            try:
                espera_elemento(self.WDW180, (By.CSS_SELECTOR, '#completed_window'))
            except TimeoutException:
                raise Exception('Não foi possível fazer o OCR... Provavelmenten não encontrou nenhum texto.')

            verifica_se_baixou_o_arquivo(self.DOWNLOAD_DIR, '.txt')            
            self.DRIVER.close()
        except Exception as e:
            print('Ocorreu um erro!')
            print(str(e))
            

            
    def recupera_texto(self) -> str:
        try:
            file_txts = arquivos_com_caminho_absoluto_do_arquivo(self.DOWNLOAD_DIR)
            file_txt = file_txts[-1]
            text = None
            with open(file_txt, mode='r', encoding='utf-16-le') as f:
                text = f.read()
            shutil.rmtree(self.DOWNLOAD_DIR)
            return text
        except IndexError:
            raise FalhaAoRecuperarOcr('Ocorreu um erro na recuperação que causou um IndexError, provavelmente não baixou o arquivo.')
