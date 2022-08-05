"""	
Aqui você encontrará algumas funções utilizando Regex

Se necessário, colaborem =)
"""

########### imports ##############
import re

from FuncsForSPO.functions_for_py import faz_log
########### imports ##############

def extrair_cpfs(text :str) -> list:
    """### Recupera CPF's

    Args:
        text (str): texto que vem o(s) cpf(s)

    Returns:
        list: cpf(s)
    """
    cpfs = re.findall("\d{3}.\d{3}.\d{3}-\d{2}", text)
    if not cpfs or len(cpfs) == 0:
        cpfs = re.findall("\d{3}.\d{3}.\d{3} -\d{2}", text)
        if cpfs and len(cpfs) > 0:
            a_cpfs = cpfs
            cpfs = []
            for a_cpf in a_cpfs:
                cpf = ''.join(i for i in a_cpf if i.isdigit()
                                or i in ['.', '-'])
                text = text.replace(a_cpf, cpf)
                cpfs.append(cpf)
    if not cpfs or len(cpfs) == 0:
        cpfs = []
    return cpfs


def extrair_email(text: str, case_isensitive: bool=False) -> list:
    """### Retorna os e-mails recuperados
    Validação / Busca de e-mails com o padrão RFC2822
    https://regexr.com/2rhq7

    Args:
        text (str): Texto com o(s) email(s)
        case_isensitive (bool): Buscar idependente se a letra for maiúscula ou minúscula
    Returns:
        list: email(s)
    """
    email = re.findall("[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", text, )
    if not email or len(email) == 0:
        email = []
    return email

def remove_caracteres_de_string():
    """Função remove esses elementos da string
    
    '.'
    
    '/'
    
    ','
    
    '-'
    
    '_'
    
    '='
    
    '|'
    
    '#'
    
    '`'
    
    '~'
    
    "'"
    
    '"'
    
    ';'
    
    'string'.strip()
    #### Função já converte o argumento para str()

    Args:
        string (str): str com os caracteres

    Returns:
        str: Retorna string sem nenhum desses caracteres
    """
    string = str(string)
    string = string.replace('.','')
    string = string.replace('/', '')
    string = string.replace(',', '')
    string = string.replace('-', '')
    string = string.replace('_', '')
    string = string.replace('=', '')
    string = string.replace('|', '')
    string = string.replace('`', '')
    string = string.replace('~', '')
    string = string.replace("'", '')
    string = string.replace('"', '')
    string = string.replace('#', '')
    string = string.replace(';', '')
    string = string.replace(':', '')
    string = string.strip()
    return string


def extrair_numeros(str, return_first=True) -> list[str]|str:
    """Recupera somente números de uma string

    Args:
        str (string): string com os números
        return_first (bool, optional): retorna o primeiro conjunto de números. Defaults to True.

    Returns:
        list|str: lista com os números ou ou uma string com os números
    """
    if return_first:
        return re.findall('\d+', str)[0]  # return str
    else:
        return re.findall('\d+', str) # return list


def extrair_num_processo(text: str) -> list:
    """### Retorna o(s) número(s) de processo(s)

    Args:
        text (str): texto com o(s) ñ de processo(s)

    Returns:
        list: número(s) de processo(s)
    """
    processo = re.search("\d{7}-\d{2}.\d{4}.\d{1}.\d{2}.\d{4}", text)
    if processo:
        processo = processo.group()
    else:
        processo = ''
    return processo


def extrair_cnpjs(text: str) -> list:
    """### Recupera cnpj(s) da string

    Args:
        text (str): texto que pode haver cnpj(s)

    Returns:
        list: cnpj(s)
    """
    cnpjs = re.findall("\d{2}.\d{3}.\d{3}/\d{4}-\d{2}", text)    
    if not cnpjs or len(cnpjs) == 0:
        cnpjs = []
    return cnpjs, text


def extrair_datas(text: str) -> str:
    """### Retorna datas no padrão \d{2}/\d{2}/\d{4} -> 00/00/0000

    Args:
        text (str): texto que tem datas

    Returns:
        list: data(s)
    """
    datas = re.findall("\d{2}/\d{2}/\d{4}", text.lower())    
    if not datas or len(datas) == 0:
        datas = []
    return datas


def pega_id(assunto: str) -> str:
    """
    Essa função simplesmente pega uma string, separa ela por espaços e verifica se a palavra existe ou é igual a "ID",
        se existe, pega a string, caso seja igual, pega a string e um acima para pegar o id em si

    Args:
        assunto (str): Assunto do E-mail

    Returns:
        str | bool: Retorna o id com o número ou False se não tiver um assunto com ID
    """
    assunto = assunto.upper()
    assunto = assunto.strip()
    list_string_official = []
    if 'ID' in assunto:
        # Separa todos as strings por espaço
        assunto_list = assunto.split(' ')

        for i in range(len(assunto_list)):
            # se a palavra do assunto for id e a próxima palavra for 'elaw' pega id e o número
            if assunto_list[i] == 'ID' and assunto_list[i+1] == 'ELAW':
                list_string_official.append(assunto_list[i])
                list_string_official.append(assunto_list[i+2])
                id_ = ' '.join(list_string_official)
                faz_log(id_)
                return id_
            if assunto_list[i] == 'ID' and 'ELAW' in assunto_list[i+1]:
                list_string_official.append(assunto_list[i])
                try:
                    list_string_official.append(assunto_list[i+2])
                except Exception:
                    list_string_official.append(assunto_list[i+1])
                    id_ = ' '.join(list_string_official)
                    num_id = re.findall(r'\d+', id_)  # pega somente números da string
                    id_ = f'ID {num_id[0]}'#EX (ID 111111)#
                    faz_log(id_)
                    return id_
                id_ = ' '.join(list_string_official)
                faz_log(id_)
                return id_
            if assunto_list[i] == 'ID' or assunto_list[i] == 'ID:' or assunto_list[i] == 'ID.' or assunto_list[i] == '-ID':
                list_string_official.append(assunto_list[i])
                list_string_official.append(assunto_list[i+1])
                id_ = ' '.join(list_string_official)
                faz_log(id_)
                return id_
        else:
            faz_log(f'Não existe ID para o ASSUNTO: {assunto}', 'w')
            return False
    else:
        faz_log(f'Não existe ID para o ASSUNTO: {assunto}', 'w')
        return False


def extrair_ids(text: str) -> tuple[list, int]:
    """Extrair IDS do Elaw

    Args:
        text (str): texto que ter

    Returns:
        tuple[list, int]: _description_
    """
    ids = re.findall("id: \d+|id elaw\d+|id elaw \d+|id \d+|id - \d+", text, flags=re.IGNORECASE)
    if not ids or len(ids) == 0:
        ids = []
    return ids, len(ids)
