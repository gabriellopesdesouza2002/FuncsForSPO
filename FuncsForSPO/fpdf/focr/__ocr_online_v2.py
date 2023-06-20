from FuncsForSPO.fpdf.focr.base import *

class OCRPDFV2(BotMain):    
    def __init__(self, file_pdf: str, headless: bool=True) -> str:
        self.PDF_PATH = os.path.abspath(file_pdf)
        self.HEADLESS = headless
        super().__init__(self.HEADLESS)
    
    def run(self):
        try:
            self.DRIVER.get('https://ocrpaycon.streamlit.app/')
            self.DRIVER.switch_to.frame(espera_elemento(self.WDW10, (By.CSS_SELECTOR, 'iframe[title="streamlitApp"]'), in_dom=True))
            espera_elemento(self.WDW, (By.CSS_SELECTOR, 'input[type="file"]'), in_dom=True)
            self.DRIVER.find_element(By.CSS_SELECTOR, 'input[type="file"]').send_keys(self.PDF_PATH)
            text = espera_e_retorna_elemento_text(self.WDW420, (By.CSS_SELECTOR, 'code'), in_dom=True)
            return text
        except Exception as e:
            faz_log(repr(e), 'c*')
            faz_log(self.DRIVER.get_screenshot_as_base64(), 'i*')
            self.DRIVER.quit()
            raise ErroPDFAIException