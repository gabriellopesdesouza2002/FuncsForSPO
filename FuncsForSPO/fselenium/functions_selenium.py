from base64 import b64decode
import json
import os
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome 
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager 
from fake_useragent import UserAgent
from time import sleep
from FuncsForSPO.fpython.functions_for_py import cria_dir_no_dir_de_trabalho_atual, cria_o_ultimo_diretorio_do_arquivo, faz_log, transforma_lista_em_string
from FuncsForSPO.fregex.functions_re import extrair_email
from wget import download

def url_atual(driver) -> str:
    """
    ### Função RETORNA a url atual

    Args:
        driver (WebDriver): Seu Webdriver (Chrome, Firefox, Opera...)

    Returns:
        (str): URL atual da janela atual
    """
    return driver.current_url


def atualiza_page_atual(driver) -> None:
    """
    ### Função atualiza a página atual da janela atual

    Args:
        driver (WebDriver): Seu Webdriver (Chrome, Firefox, Opera...)
        
    """
    driver.refresh()
        
        
def espera_e_clica_em_varios_elementos(driver, wdw, locator: tuple) -> None:
    
    wdw.until(EC.presence_of_all_elements_located(locator))
    elements = driver.find_elements(*locator)
    len_elements = len(elements)

    for i in range(len_elements):
        elements[i].click()
        
        
def verifica_se_baixou_o_arquivo(diretorio_de_download, palavra_chave):
    _LOCAL_DE_DOWNLOAD = os.path.abspath(diretorio_de_download)
    baixou = False
    while not baixou:
        lista_arquivos = os.listdir(_LOCAL_DE_DOWNLOAD)
        if len(lista_arquivos) == 0:
            sleep(2)
            baixou = False
            lista_arquivos = os.listdir(_LOCAL_DE_DOWNLOAD)
        else:
            for i in lista_arquivos:
                if '.crdownload' in i:
                    sleep(2)
                    lista_arquivos = os.listdir(_LOCAL_DE_DOWNLOAD)
                    baixou = False
                    continue
                if palavra_chave in i:
                    baixou = True
                    faz_log('Download concluido!')
                    return True
                else:
                    sleep(2)
                    lista_arquivos = os.listdir(_LOCAL_DE_DOWNLOAD)
                    baixou = False
        
def espera_elemento_disponivel_e_clica(wdw, locator: tuple) -> None:
    """Espera o elemento ficar disponível para clicar e clica

    Args:
        wdw (WebDriverWait): WebDriverWait
        locator (tuple): localização do elemento -> (By.CSS_SELECTOR, '.b')
    """
    wdw.until(EC.element_to_be_clickable(locator)).click()


def espera_elemento(wdw, locator: tuple) -> WebElement:
    """
    ### Função que espera pelo elemento enviado do locator

    Args:
        wdw (WebDriverWait): Seu WebDriverWait
        locator (tuple): A localização do elemento no DOM (By.CSS_SELECTOR, '#IdButton')
        
    """
    return wdw.until(EC.element_to_be_clickable(locator))


def set_zoom_page(driver, zoom: int):
    """Seta o zoom da página atual

    Args:
        driver (WebDriver): WebDriver
        zoom (int): O zoom para setar.
    """
    driver.execute_script(f"document.body.style.zoom='{zoom}%'")


def espera_2_elementos(wdw, locator1: tuple, locator2 : tuple) -> WebElement:
    """
    ### Função que espera pelo elemento enviado do locator

    Args:
        wdw (WebDriverWait): Seu WebDriverWait
        locator (tuple): A localização do elemento no DOM (By.CSS_SELECTOR, '#IdButton')
        
    """
    try:
        wdw.until(EC.element_to_be_clickable(locator1))
    except Exception:
        wdw.until(EC.element_to_be_clickable(locator2))
        
        
def download_wget(url: str, out: str | None=None):
    """Faz download via URL

    Args:
        url (str): _description_
        out (str | None, optional): _description_. Defaults to None.
    """
    return download(url, out)


def espera_elemento_e_envia_send_keys(driver, wdw, string, locator: tuple) -> None:
    """
    ### Função que espera pelo elemento enviado do locator e envia o send_keys no input ou textarea assim que possível

    Args:
        driver (WebDriver): Seu Webdriver (Chrome, Firefox, Opera)
        wdw (WebDriverWait): Seu WebDriverWait
        locator (tuple): A localização do elemento no DOM (By.CSS_SELECTOR, '#IdButton')
        
    """
    wdw.until(EC.element_to_be_clickable(locator))
    try:
        driver.find_element(*locator).send_keys(string)
    except StaleElementReferenceException:
        wdw.until(EC.element_to_be_clickable(locator))
        driver.find_element(*locator).send_keys(string)
    
    
def set_zoom_page(driver, zoom: int):
    """Seta o zoom da página atual

    Args:
        driver (WebDriver): WebDriver
        zoom (int): O zoom para setar.
    """
    driver.execute_script(f"document.body.style.zoom='{zoom}%'")
    
    
def espera_e_retorna_lista_de_elementos(driver, wdw, locator: tuple) -> list:
    """
    ### Função espera e retorna uma lista de elementos indicados no locator

    Args:
        driver (Webdriver): Seu Webdriver (Chrome, Opera, Firefox)
        wdw (WebDriverWait): Seu WebDriverWait
        locator (tuple): A tupla indicando a localização do elemento no DOM ("BY_SELECTOR", "#list_arms").

    Returns:
        list: Lista com os elementos com o formato de Objetos (lista de Objetos)
    """
    wdw.until(EC.element_to_be_clickable(locator))
    return driver.find_elements(*locator)

def download_de_arquivo_em_sharepoint(headless, pasta_de_download_e_print, url_file, email, passwd):
    """de uma forma bem grotesca fazendo um download de um arquivo compartilhado
    pode ser utilizado para arquivos que tem que ter o navegador aberto para fazer o download

    Args:
        headless (bool): executar como headless
        pasta_de_download_e_print (str): local de download
        pasta_de_download_e_print (url): url para dar get
        pasta_de_download_e_print (int|float): tempo para esperar na Thread atual
    """
    from selenium.webdriver import Chrome
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.support.wait import WebDriverWait
    from webdriver_manager.chrome import ChromeDriverManager
    import json
    import shutil
    
    # pasta de download como relativa, pois cria no dir de trabalho atual
    # --- CHROME OPTIONS --- #
    options = ChromeOptions()

    # --- PATH BASE DIR --- #
    if os.path.exists(pasta_de_download_e_print):
        shutil.rmtree(pasta_de_download_e_print)
        sleep(1)
        DOWNLOAD_DIR = cria_dir_no_dir_de_trabalho_atual(dir=pasta_de_download_e_print, print_value=False, criar_diretorio=True)
    else:        
        DOWNLOAD_DIR = cria_dir_no_dir_de_trabalho_atual(dir=pasta_de_download_e_print, print_value=False, criar_diretorio=True)

    SETTINGS_SAVE_AS_PDF = {
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

    PROFILE = {'printing.print_preview_sticky_settings.appState': json.dumps(SETTINGS_SAVE_AS_PDF),
                "savefile.default_directory":  f"{DOWNLOAD_DIR}",
                "download.default_directory":  f"{DOWNLOAD_DIR}",
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True}

    options.add_experimental_option('prefs', PROFILE)

    options.add_experimental_option(
        "excludeSwitches", ["enable-logging"])
    if headless:
        options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-webgl")
        options.add_argument('--disable-gpu')
    options.add_argument('--kiosk-printing')
    options.add_argument("--start-maximized")

    service = Service(executable_path=ChromeDriverManager().install())

    DRIVER = Chrome(service=service, options=options)
    DRIVER.maximize_window()
    WDW = WebDriverWait(DRIVER, 5)
    try:
        DRIVER.get(url_file)
        
        faz_log(f'Enviando Usuário...')
        try:
            espera_elemento_e_envia_send_keys(DRIVER, WDW, email, (By.CSS_SELECTOR, '#i0116'))
        except TimeoutException:
            try:
                espera_elemento_e_envia_send_keys(DRIVER, WDW, email, (By.CSS_SELECTOR, 'input[data-report-event*="Signin_Email"]'))
            except TimeoutException:
                espera_elemento_e_envia_send_keys(DRIVER, WDW, email, (By.CSS_SELECTOR, 'input[name*="loginfmt"]'))

        # clica em Avançar
        try:
            espera_elemento_disponivel_e_clica(WDW, (By.CSS_SELECTOR, '#idSIButton9'))
        except TimeoutException:
            espera_elemento_disponivel_e_clica(WDW, (By.CSS_SELECTOR, 'input[data-report-event*="Submit"]'))

        # Envia _SENHA
        faz_log(f'Enviando Senha Elaw...')
        try:
            espera_elemento_disponivel_e_clica(WDW, (By.CSS_SELECTOR, 'div[role="button"]'))
        except TimeoutException:
            ...
        try:
            espera_elemento_e_envia_send_keys(DRIVER, WDW, passwd, (By.CSS_SELECTOR, '#i0118'))
        except TimeoutException:
            try:
                espera_elemento_e_envia_send_keys(DRIVER, WDW, passwd, (By.CSS_SELECTOR, 'input[type="password"]'))
            except TimeoutException:
                espera_elemento_e_envia_send_keys(DRIVER, WDW, passwd, (By.CSS_SELECTOR, 'input[data-bind*="password"]'))
        except StaleElementReferenceException:
            espera_elemento_e_envia_send_keys(DRIVER, WDW, passwd, (By.CSS_SELECTOR, '#i0118'))

        # clica em Entrar
        faz_log(f'Clicando em "Entrar"...')
        try:
            espera_elemento_disponivel_e_clica(WDW, (By.CSS_SELECTOR, '#idSIButton9'))
        except TimeoutException:
            espera_elemento_disponivel_e_clica(WDW, (By.CSS_SELECTOR, 'input[data-report-event*="Submit"]'))

        # clica em Sim
        faz_log(f'Clicando em "Sim"...')
        try:
            espera_elemento_disponivel_e_clica(WebDriverWait(DRIVER, 10), (By.CSS_SELECTOR, '#idSIButton9'))
        except TimeoutException:
            espera_elemento_disponivel_e_clica(WebDriverWait(DRIVER, 10), (By.CSS_SELECTOR, 'input[data-report-event*="Submit"]'))
            
        baixou = False
        while baixou == False:
            list_dir = os.listdir(pasta_de_download_e_print)
            if len(list_dir) >= 1:
                list_dir = os.listdir(pasta_de_download_e_print)
                for i in list_dir:
                    if '.crdownload' in i:
                        list_dir = os.listdir(pasta_de_download_e_print)
                        baixou = False
                    else:
                        list_dir = os.listdir(pasta_de_download_e_print)
                        baixou = True
            else:
                list_dir = os.listdir(pasta_de_download_e_print)
                baixou = False
    except TimeoutException:
        DRIVER.quit()
        download_de_arquivo_em_sharepoint(headless, pasta_de_download_e_print, url_file, email, passwd)
            

def download_de_arquivo_com_link_sem_ext_pdf(link: str, driver, back_to_page: bool=False):
    """Faz download do pdf com o link do href, ele entrará no pdf e dará print_page

    Args:
        link (str): link do arquivo que deseja baixar
        driver (WebDriver): Driver
        back_to_page (bool): Se deseja voltar para a page anterior. Optional, default is False

    Use:
        >>> link = espera_e_retorna_conteudo_do_atributo_do_elemento_text(DRIVER, WDW3, 'href', (By.CSS_SELECTOR, 'div>a'))
        >>> download_de_arquivo_com_link_sem_ext_pdf(link, mywebdriver, False)
    
    """
    driver.get(link)
    sleep(3)
    driver.print_page()
    if back_to_page:
        driver.back()
        driver.refresh()



def espera_e_retorna_lista_de_elementos_text_from_id(driver, wdw, locator: tuple) -> list:
    """
    ### Função espera e retorna uma lista de elementos com id
    

    Args:
        driver (WebDriver): Seu Webdriver (Chrome, Firefox, Opera)
        wdw (WebDriverWait): Seu WebDriverWait
        locator (tuple): A tupla indicando a localização do elemento no DOM ("BY_SELECTOR", "#list_arms").

    Returns:
        list: Lista de textos dos elementos com id -> [adv 1, adv 2, adv 3, adv 4, adv 5]
    """
    wdw.until(EC.element_to_be_clickable(locator))
    webelements = driver.find_elements(*locator)
    id = 1
    elementos_com_id = []
    for element in webelements:
        if element.text == ' ':
            elementos_com_id.append(element.text)
        else:
            elementos_com_id.append(f'{element.text} {id}')
        id += 1
    else:
        return elementos_com_id

    
# utilizado para o STJ   
# def espera_e_retorna_lista_de_elementos_text_from_id_esse_tribunal(driver, wdw, locator: tuple=("BY_SELECTOR", "WEBELEMENT")):
#     """Função espera e retorna 

#     Args:
#         driver (WebDriver): _description_
#         wdw (WebDriverWait): _description_
#         locator (tuple, optional): _description_. Defaults to ("BY_SELECTOR", "WEBELEMENT").

#     Returns:
#         list: lista_de_elementos_text_from_id_esse_tribunal
#     """
#     if locator == ("BY_SELECTOR", "WEBELEMENT"):
#         print('Adicione um locator!!!!')
#         return
#     wdw.until(EC.element_to_be_clickable(locator))
#     webelements = driver.find_elements(*locator)
#     id = 1
#     elementos_com_id = []
#     for element in webelements:
#         if element.text == ' ':
#             elementos_com_id.append(f'VOLUME(S) col{id}')
#         else:
#             elementos_com_id.append(f'{element.text} col{id}')
#         id += 1
#     else:
#         return elementos_com_id


def espera_e_retorna_lista_de_elementos_text(driver, wdw, locator: tuple, upper_mode :bool=False, strip_mode :bool=False) -> list:
    """
    ### Função espera e retorna uma lista com os textos dos elementos

    Args:
        driver (Webdriver): Seu Webdriver (Chrome, Firefox, Opera)
        wdw (WebDriverWait): Seu WebDriverWait
        locator (tuple): A tupla indicando a localização do elemento no DOM ("BY_SELECTOR", "#list_arms").

    Returns:
        list: Lista dos textos dos elementos
    """
    wdw.until(EC.element_to_be_clickable(locator))
    elements = driver.find_elements(*locator)
    if upper_mode:
        elements_not_upper = [element.text for element in elements]
        return [element.upper() for element in elements_not_upper]
    if strip_mode:
        elements_not_strip = [element.text for element in elements]
        return [element.strip() for element in elements_not_strip]
    return [element.text for element in driver.find_elements(*locator)]


def espera_elemento_ficar_visivel(driver, wdw, locator: tuple) -> WebElement|None:
    """Espera elemento ficar visivel na tela

    Args:
        driver (WebDriver): Webdriver
        wdw (WebDriverWait): WDW
        locator (tuple): Locator

    Returns:
        WebElement|None: WebElement or None
    """
    element = driver.find_element(*locator)
    return wdw.until(EC.visibility_of(element))


def baixa_pdf_via_base64_headless_only(driver: WebDriver, file_pdf_with_extension: str='MyPDF.pdf', locator: tuple=(By.CSS_SELECTOR, 'html')):
    """
    ## Funciona somente com headless!
    é necessário que o driver já esteja aberto, passando somente o locator que deseja converter para pdf
    
        creditos
        https://stackoverflow.com/questions/66682962/headless-chrome-webdriver-issue-after-printing-the-web-page
    Args:
        file_pdf_with_extension (str, optional): _description_. Defaults to 'MyPDF.pdf'.
        locator (tuple, optional): _description_. Defaults to (By.CSS_SELECTOR, 'html').

    Raises:
        ValueError: _description_
    """
    FILE_PDF = os.path.abspath(file_pdf_with_extension)
    element = driver.find_element(*locator)
    ActionChains(driver).click(element).click_and_hold().move_by_offset(0, 0).perform()

    element = driver.execute_cdp_cmd(
        "Page.printToPDF", {"path": 'html-page.pdf', "format": 'A4'})
    # Importar apenas a função b64decode do módulo base64

    # Defina a string Base64 do arquivo PDF
    b64 = element['data']

    # Decode the Base64 string, making sure that it contains only valid characters
    bytes = b64decode(b64, validate=True)

    # Execute uma validação básica para garantir que o resultado seja um arquivo PDF válido
    # Estar ciente! O número mágico (assinatura do arquivo) não é uma solução 100% confiável para validar arquivos PDF
    #Além disso, se você obtiver Base64 de uma fonte não confiável, deverá higienizar o conteúdo do PDF
    if bytes[0:4] != b'%PDF':
        raise ValueError('Missing the PDF file signature')

    # Write the PDF contents to a local file
    try:
        with open(FILE_PDF, 'wb') as f:
            f.write(bytes)
    except FileNotFoundError:
        cria_o_ultimo_diretorio_do_arquivo(FILE_PDF)
        with open(FILE_PDF, 'wb') as f:
            f.write(bytes)


def verifica_se_esta_conectado_na_vpn(ping_host :str):
    from subprocess import getoutput
    PING_HOST = ping_host
    """O método verificará por ping se está conectado no ip da VPN"""

    faz_log('Verificando se VPN está ativa pelo IP enviado no config.ini')
    
    output = getoutput(f'ping {PING_HOST} -n 1')  # -n 1 limita a saída
    if 'Esgotado o tempo' in output or 'time out' in output:
        faz_log('VPN NÃO CONECTADA!', 'w')
    else:
        faz_log("VPN conectada com sucesso!")



def espera_elemento_ficar_visivel_ativo_e_clicavel(driver, wdw, locator: tuple) -> WebElement|None:
    """Espera Elemento ficar visivel, ativo e clicavel

    Args:
        driver (Webdriver): Webdriver
        wdw (WDW): WDW
        locator (tuple): Locator Selenium

    Returns:
        WebElement|None: _description_
    """
    element = driver.find_element(*locator)
    wdw.until(EC.element_to_be_clickable(locator))
    return wdw.until(EC.visibility_of(element))


def espera_e_retorna_conteudo_do_atributo_do_elemento_text(driver, wdw, atributo, locator: tuple) -> str:
    """
    ### Função que espera pelo elemento e retorna o texto do atributo do elemento escolhido

    Args:
        driver (Webdriver): Seu Webdriver (Chrome, Firefox)
        wdw (WebDriverWait): Seu WebDriverWait
        atributo (str): O atributo que deseja recuperar, como um href, id, class, entre outros
        locator (tuple): A localização do elemento no DOM ("By.CSS_SELECTOR", "body > div > a").

    Returns:
        str: retorna uma string com o valor do atributo do elemento
    """
    wdw.until(EC.element_to_be_clickable(locator))
    return driver.find_element(*locator).get_attribute(atributo)


def espera_e_retorna_conteudo_dos_atributos_dos_elementos_text(driver, wdw, atributo, locator: tuple) -> list:
    """
    ### Função espera e retorna o valor dos atributos de vários elementos

    Args:
        driver (Webdriver): Seu Webdriver (Chrome, Firefox)
        wdw (WebDriverWait): Seu WebDriverWait
        atributo (str): Atributo (esse deve existir em todos os elementos)
        locator (tuple): Posição dos elementos no DOM.("By.CSS_SELECTOR", "#list_works").

    Returns:
        list: Lista com os atributos de todos os elementos (é necessário que o atibuto enviado exista em todos os elementos como um href)
    """
    wdw.until(EC.element_to_be_clickable(locator))
    atributos = driver.find_elements(*locator)
    elementos_atributos = [atributo_selen.get_attribute(atributo) for atributo_selen in atributos]
    return elementos_atributos
        
        
def espera_e_retorna_elemento_text(driver,  wdw, locator: tuple) -> str:
    """Função espera o elemento e retorna o seu texto

    Args:
        driver (Webdriver): Webdriver (Chrome, Firefox)
        wdw (WebDriverWait): WebDriverWait
        locator (tuple): Localização do elemento no DOM. ("By.CSS_SELECTOR", "#name")

    Returns:
        str: Retorna a string de um elemento
    """
    wdw.until(EC.element_to_be_clickable(locator))
    return driver.find_element(*locator).text
    
    
def vai_para_a_primeira_janela(driver) -> None:
    """Vai para a primeira janela, geralmente a primeira que é iniciada

    Args:
        driver (WebDriver): WebDriver
    """
    window_ids = driver.window_handles # ids de todas as janelas
    driver.switch_to.window(window_ids[0])
    
    
def espera_abrir_n_de_janelas_e_muda_para_a_ultima_janela(driver, wdw, num_de_janelas: int=2) -> None:
    """Função espera abrir o numero de janelas enviada por ti, e quando percebe que abriu, muda para a última janela aberta

    Args:
        driver (Webdriver): Webdriver (Chrome, Firefox)
        wdw (WebDriverWait): WebDriver
        num_de_janelas (int): Quantidade de janelas esperadas para abrie. O padrão é 2.
    """
    print(f'Você está na janela -> {driver.current_window_handle}')
    wdw.until(EC.number_of_windows_to_be(num_de_janelas))
    print(f'Agora, você tem {len(driver.window_handles)} janelas abertas')
    todas_as_windows = driver.window_handles
    driver.switch_to.window(todas_as_windows[-1])
    print(f'Agora, você está na janela -> {driver.current_window_handle}')
    
    
def procura_pela_janela_que_contenha_no_titulo(driver, title_contain_switch : str) -> None: # quero que pelo menos um pedaco do titulo que seja str
    """
    ### Essa função muda de janela quando o título tiver pelo menos algo igual ao parametro enviado
    #### Ex -> Minha janela = janela
    
    Args:
        driver (Webdriver): Webdriver (Chrome, Firefox)
        title_contain_switch (str) : Pelo menos um pedaco do titulo exista para mudar para a página 
    """
    window_ids = driver.window_handles # ids de todas as janelas

    for window in window_ids:
        driver.switch_to_window(window)  
        if title_contain_switch in driver.title:
            break
    else:
        print(f'Janela não encontrada!\n'
            f'Verifique o valor enviado {title_contain_switch}')
    
    
def fecha_janela_atual(driver) -> None:
    """
    ### Função que fecha a janela atual

    Args:
        driver (WebDriver): Seu WebDriver (Chrome, Firefox)
    """
    driver.close()


def fecha_ultima_janela(driver) -> None:
    qtd_de_windows = driver.window_handles
    while len(qtd_de_windows) !=2:
        qtd_de_windows = driver.window_handles
    else:
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])


def espera_enquanto_nao_tem_resposta_do_site(driver, wdw, locator : tuple) -> None:
    """
    ### Função que espera enquanto o site não tem resposta
    
    #### ESSA FUNÇÃO SÓ DEVE SER USADA CASO VOCÊ TENHA CERTEZA QUE O SITE POSSA VIR A CAIR

    Args:
        driver (WebDriver): Seu WebDriver (Chrome, Firefox)
        wdw (WebDriverWait): WebDriverWait
        locator (tuple): Localização do elemento no DOM. ("By.CSS_SELECTOR", "#ElementQueSempreEstaPresente")
    """
    try:
        element = wdw.until(EC.element_to_be_clickable(locator))
        if element:
            return element
    except TimeoutException:
        print('Talvez a página tenha dado algum erro, vou atualiza-lá')
        sleep(2)
        try:
            driver.refresh()
            element = wdw.until(EC.element_to_be_clickable(locator))
            if element:
                print('Voltou!')
                return element
        except TimeoutException:
            print('A página ainda não voltou, vou atualiza-lá')
            sleep(2)
            try:
                driver.refresh()
                element = wdw.until(EC.element_to_be_clickable(locator))
                if element:
                    print('Voltou!')
                    return element
            except TimeoutException:
                print('Poxa, essa será a última vez que vou atualizar a página...')
                sleep(2)
                try:
                    driver.refresh()
                    element = wdw.until(EC.element_to_be_clickable(locator))
                    if element:
                        print('Voltou!')
                        return element
                except TimeoutException:
                    print("Olha, não foi possível. A página provavelmente caiu feio :(")
                    print("Infelizmente o programa vai ser finalizado...")
                    driver.quit()
                   
                   
def volta_paginas(driver, qtd_pages_para_voltar : int=1, espera_ao_mudar=0) -> None:
    """
    ### Essa função volta (back) quantas páginas você desejar

    Args:
        driver (WebDriver): Seu webdriver
        qtd_pages_para_voltar (int): Quantidade de páginas que serão voltadas. O padrão é uma página (1).
        espera_ao_mudar (int or float, optional): Se você quer esperar um tempo para voltar uma página. O padrão é 0.
        
    Uso:
        volta_paginas(driver=chrome, qtd_pages_para_voltar=3, espera_ao_mudar=1)
    """
    if espera_ao_mudar == 0:
        for back in range(qtd_pages_para_voltar):
            driver.back()
            driver.refresh()
    else:
        for back in range(qtd_pages_para_voltar):
            sleep(espera_ao_mudar)
            driver.back()
            driver.refresh()
    
    
# Em desenvolvimento
    
# def muda_p_alerta_e_clica_em_accept(driver, wdw, sleeping):
    # sleep(sleeping)
    # alerta = driver.switch_to.alert
    # alerta.accept()


# def muda_p_alerta_e_clica_em_dismiss(self):
    # alerta = chrome.switch_to.alert
    # alerta.dismiss()

    
# Em desenvolvimento

def cria_user_agent() -> str:
    """Cria um user-agent automaticamente com a biblio fake_useragent

    Use:
        https://stackoverflow.com/questions/48454949/how-do-i-create-a-random-user-agent-in-python-selenium

    Returns:
        str: user_agent
    """
    _ua = UserAgent()
    user_agent = _ua.random
    return user_agent


def espera_input_limpa_e_envia_send_keys_preessiona_esc(driver, wdw, keys : str, locator : tuple) -> None:
    from selenium.common.exceptions import StaleElementReferenceException
    from selenium.webdriver.common.keys import Keys

    """
    ### Função espera pelo input ou textarea indicado pelo locator, limpa ele e envia os dados

    Args:
        driver (WebDriver): Seu webdriver
        wdw (WebDriverWait): WebDriverWait criado em seu código
        keys (str): Sua string para enviar no input ou textarea
        locator (tuple): Tupla que contém a forma e o caminho do elemento (By.CSS_SELECTOR, '#myelementid')
    """
    try:
        wdw.until(EC.element_to_be_clickable(locator))
        driver.find_element(*locator).click()
        driver.find_element(*locator).send_keys(Keys.ESCAPE)
        driver.find_element(*locator).clear()
        driver.find_element(*locator).send_keys(keys)
    except StaleElementReferenceException:
        wdw.until(EC.element_to_be_clickable(locator))
        driver.find_element(*locator).click()
        driver.find_element(*locator).send_keys(Keys.ESCAPE)
        driver.find_element(*locator).clear()
        driver.find_element(*locator).send_keys(keys)

    
def espera_input_limpa_e_envia_send_keys(driver, wdw, keys : str, locator : tuple, click: bool=True) -> None:
    from selenium.common.exceptions import StaleElementReferenceException
    """
    ### Função espera pelo input ou textarea indicado pelo locator, limpa ele e envia os dados

    Args:
        driver (WebDriver): Seu webdriver
        wdw (WebDriverWait): WebDriverWait criado em seu código
        keys (str): Sua string para enviar no input ou textarea
        locator (tuple): Tupla que contém a forma e o caminho do elemento (By.CSS_SELECTOR, '#myelementid')
        click (bool): Clica ou não no elemento
    """
    try:
        wdw.until(EC.element_to_be_clickable(locator))
        if click:
            driver.find_element(*locator).click()
        driver.find_element(*locator).clear()
        driver.find_element(*locator).send_keys(keys)
    except StaleElementReferenceException:
        wdw.until(EC.element_to_be_clickable(locator))
        if click:
            driver.find_element(*locator).click()
        driver.find_element(*locator).clear()
        driver.find_element(*locator).send_keys(keys)
    
        
def espera_elemento_sair_do_dom(wdw, locator) -> WebElement:
    return wdw.until_not(EC.presence_of_element_located(locator))
    

def pega_somente_numeros_de_uma_str(string) -> list:
    """
    ### Função que retorna uma LISTA somente com os números de uma string
    #### Removida do site: https://www.delftstack.com/pt/howto/python/python-extract-number-from-string/#:~:text=Utilizar%20a%20Compreens%C3%A3o%20da%20Lista,%C3%A9%20encontrado%20atrav%C3%A9s%20da%20itera%C3%A7%C3%A3o.
       
    Args:
        string (str): String que tem números com letras
    """
    numbers = [int(temp) for temp in string.split() if temp.isdigit()]
    return numbers
    
    
def espera_elemento_ficar_ativo_e_clica(driver, wdw, locator : tuple) -> None:

    wdw.until_not(EC.element_to_be_selected(driver.find_element(*locator)))
            # qualquer h1 que aparecer vai falar (apareceu)

    print('O Botão está ativo')

    driver.find_element(*locator).click()
        
        
def espera_elemento_nao_estar_mais_visivel(wdw, locator) -> WebElement:
    return wdw.until_not(EC.visibility_of(*locator))
    
    
def espera_elemento_estar_visivel(driver, wdw, locator, with_visibility_of: bool=True):
    if with_visibility_of:
        element = driver.find_element(*locator)
        return wdw.until(EC.visibility_of(element))
    else:
        element = driver.find_element(*locator)
        return wdw.until(EC.element_to_be_clickable(locator))
        


def find_window_to_title_contain(driver, title_contain_switch: str) -> None: # quero que pelo menos um pedaco do titulo que seja str
    """
    ### Essa função muda de janela quando o título tiver pelo menos algo igual ao parametro enviado
    #### Ex -> Minha janela = janela
    
    para cada janela em ids das janelas
    muda para a janela
    se a janela for ao menos de um pedaço do titulo que passei
        em title_contain_switch
    para de executar
    """
    window_ids = driver.window_handles # ids de todas as janelas

    for window in window_ids:
        driver.switch_to_window(window)  
        if title_contain_switch in driver.title:
            break
    else:
        print(f'Janela não encontrada!\n'
              f'Verifique o valor enviado {title_contain_switch}')
    
    
def find_window_to_url(driver, url_switch: str) -> None: # quero uma url que seja str
    """
    ### Essa função muda de janela quando a url for igual ao parametro enviado
    #### Ex -> https://google.com.br  = https://google.com.br
    
    para cada janela em ids das janelas
    muda para a janela
    se a janela for do titulo que passei
        em title_switch
    para de executar
    """
    window_ids = driver.window_handles # ids de todas as janelas

    for window in window_ids:
        driver.switch_to_window(window)
        if driver.current_url == url_switch:
            break
        else:
            print(f'Janela não encontrada!\n'
                f'Verifique o valor enviado "{url_switch}"')
    
          
def find_window_to_url_contain(driver, contain_url_switch: str) -> None: # quero uma url que seja str
    """
    ### Essa função muda de janela quando a url conter no parametro enviado
    #### Ex -> https://google.com.br  = google
    
    para cada janela em ids das janelas
    muda para a janela
    se a janela for do titulo que passei
        em title_switch
    para de executar
    """
    window_ids = driver.window_handles # ids de todas as janelas

    for window in window_ids:
        driver.switch_to.window(window)
        if contain_url_switch in driver.current_url:
            break
        else:
            print(f'Janela não encontrada!\n'
                f'Verifique o valor enviado "{contain_url_switch}"')
        
        
# def avisa_quando_fecha_janela(wdw, num_de_janelas: int=2):
#     qtd_janelas = wdw.until(EC.number_of_windows_to_be(num_de_janelas))
    
#     if qtd_janelas == num_de_janelas:
#         if wdw.until(EC.new_window_is_opened(2))
    
#     tentativas = 10
    
#     while tentativas != 0:
#         sleep(1)
#         if qtd_janelas == num_de_janelas:
#             while qtd_janelas == num_de_janelas:
#                 qtd_janelas = wdw.until(EC.number_of_windows_to_be(num_de_janelas))
#             else:
#                 return True
#         else:
#             tentativas -= 1
#             continue
#     else:
#         print('NAO ACHOU JANELAS')
        
def pega_codigo_fonte_de_elemento(driver, wdw, locator: tuple) -> str:
    """Retorna todo o código fonte do locator

    Args:
        driver (WebDriver): Webdriver
        wdw (WebDriverWait): WebDriverWait
        locator (tuple): localização do elemento no modo locator -> (By.ID, '.b')

    Returns:
        str: Código fonte do WebElement
    """
    
    wdw.until(EC.element_to_be_clickable(locator))
    element = driver.find_element(*locator)
    return element.get_attribute("outerHTML")


def verifica_se_diminuiu_qtd_de_janelas(driver, qtd_de_w) -> None:
    if len(driver.window_handles) == qtd_de_w:
        while len(driver.window_handles) >= qtd_de_w:
            ...
        else:
            window_ids = driver.window_handles # ids de todas as janelas
            driver.switch_to.window(window_ids[1])  # vai para a ultima window
            driver.close()
    else:
        verifica_se_diminuiu_qtd_de_janelas(driver, qtd_de_w)
        
            
def find_window_to_url_contain_and_close_window(driver, contain_url_to_switch: str) -> None: # quero uma url que seja str
    """
    ### Essa função muda de janela quando a url conter no parametro enviado
    #### Ex -> https://google.com.br  = google
    
    para cada janela em ids das janelas
    muda para a janela
    se a janela for do titulo que passei
        em title_switch
    para de executar
    """
    window_ids = driver.window_handles # ids de todas as janelas

    for window in window_ids:
        driver.switch_to.window(window)
        if contain_url_to_switch in driver.current_url:
            driver.close()
            break
        
def espera_input_limpa_e_envia_send_keys_preessiona_esc_tmb_no_final(driver, wdw, keys : str, locator : tuple):
    """
    ### Função espera pelo input ou textarea indicado pelo locator, limpa ele e envia os dados

    Args:
        driver (Webdriver): Seu webdriver
        wdw (WebDriverWait): WebDriverWait criado em seu código
        keys (str): Sua string para enviar no input ou textarea
        locator (tuple): Tupla que contém a forma e o caminho do elemento (By.CSS_SELECTOR, '#myelementid')
    """
    try:
        wdw.until(EC.element_to_be_clickable(locator))
        driver.find_element(*locator).click()
        driver.find_element(*locator).send_keys(Keys.ESCAPE)
        driver.find_element(*locator).clear()
        driver.find_element(*locator).send_keys(keys)
        driver.find_element(*locator).send_keys(Keys.ESCAPE)
    except StaleElementReferenceException:
        wdw.until(EC.element_to_be_clickable(locator))
        driver.find_element(*locator).click()
        driver.find_element(*locator).send_keys(Keys.ESCAPE)
        driver.find_element(*locator).clear()
        driver.find_element(*locator).send_keys(keys)
        driver.find_element(*locator).send_keys(Keys.ESCAPE)

###########################################################
######### Padrão de classe __init__ para projetos #########
###########################################################

"""
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from FuncsForSPO.fpython.functions_for_py import *
from FuncsForSPO.fselenium.functions_selenium import *
from FuncsForSPO.fexceptions.exceptions import *
import json
import os


class Bot:    
    def __init__(self, headless) -> None:
        # --- CHROME OPTIONS --- #
        options = webdriver.ChromeOptions()
        
        
        # --- PATH BASE DIR --- #
        DOWNLOAD_DIR = pega_caminho_atual_e_concatena_novo_dir(dir='base', print_value=False, criar_diretorio=True)
        SETTINGS_SAVE_AS_PDF = {
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

    
        PROFILE = {'printing.print_preview_sticky_settings.appState': json.dumps(SETTINGS_SAVE_AS_PDF),
                "savefile.default_directory":  f"{DOWNLOAD_DIR}",
                "download.default_directory":  f"{DOWNLOAD_DIR}",
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True}
            
        options.add_experimental_option('prefs', PROFILE)
        
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        if headless == 'True':
            options.add_argument('--headless')
        options.add_argument("--disable-print-preview")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--disable-extensions")
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-webgl")
        options.add_argument("--disable-popup-blocking")
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--no-proxy-server')
        options.add_argument("--proxy-server='direct://'")
        options.add_argument('--proxy-bypass-list=*')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--block-new-web-contents')
        options.add_argument('--incognito')
        options.add_argument('–disable-notifications')
        options.add_argument('--suppress-message-center-popups')
        
        service = Service(ChromeDriverManager().install())
        
    def instance_chrome(self):
        DRIVER = Chrome(service=service, options=options)
        WDW3 = WebDriverWait(DRIVER, timeout=3)
        DRIVER.maximize_window()
        return DRIVER

    def quit_web(self):
        DRIVER.quit()
"""

###########################################################
######### Padrão de classe __init__ para projetos #########
##########################################################







#######################################################################################################
######### Padrão de classe __init__ para projetos QUE TENHAM IMPRESSÃO E DOWNLOAD DE ARQUIVOS #########
#######################################################################################################
"""
from datetime import datetime
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from src.tools.functions.functions_for_py import *
from src.tools.functions.functions_selenium import *
from src.tools.functions.openpyxl_funcs import *
from FuncsForSPO.fpython.functions_for_py import faz_log
import json
import os
import pandas
import openpyxl
from src.tools.exceptions.exceptions import *


class Bot:    
    def __init__(self, configs):
        # --- PATH BASE DIR --- #
        # PATH_BASE_DIR = os.path.abspath(r".\base")

        # --- CONFIG.INI SETTINGS --- #
        config = configs
        URL = config['SECTION']['site']
        TIMEOUT = config['SECTION']['tempo_para_achar_elementos']
        HEADLESS = config['SECTION']['headless']
        USUARIO = config['SECTION']['usuario']
        SENHA = config['SECTION']['senha']
        
        # --- CHROME OPTIONS --- #
        options = webdriver.ChromeOptions()
        SETTINGS_SAVE_AS_PDF = {
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

        PROFILE = {'printing.print_preview_sticky_settings.appState': json.dumps(SETTINGS_SAVE_AS_PDF),
                "savefile.default_directory":  f"{DOWNLOAD_DIR}",
                "download.default_directory":  f"{DOWNLOAD_DIR}",
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True}
                
        options.add_experimental_option('prefs', PROFILE)
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        if HEADLESS == 'True':
            options.add_argument('--headless')
        options.add_argument("--disable-print-preview")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--disable-extensions")
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-webgl")
        options.add_argument("--disable-popup-blocking")
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--no-proxy-server')
        options.add_argument("--proxy-server='direct://'")
        options.add_argument('--proxy-bypass-list=*')
        options.add_argument('--disable-dev-shm-usage')
        
        service = Service(ChromeDriverManager().install())
        CHROME = Chrome(service=service, options=options)
        WDW = WebDriverWait(CHROME, timeout=int(TIMEOUT))
        WDW3 = WebDriverWait(CHROME, timeout=3)
        CHROME.maximize_window()
        
        # --- READ BASE --- #
        DADOS_BASE = le_base()
"""

#######################################################################################################
######### Padrão de classe __init__ para projetos QUE TENHAM IMPRESSÃO E DOWNLOAD DE ARQUIVOS #########
#######################################################################################################
