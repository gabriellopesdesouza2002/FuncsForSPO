"""
Powered by Gabriel Lopes de Souza

For use, please, install openpyxl with pip install openpyxl
"""


def get_names_worksheets(Workbook, print_value: bool=False) -> list[str]:
    """Retorna a(s) sheet(s) presentes()) na tabela

    Args:
        Workbook (Workbook, openpyxl): O Workbook
        print_value (bool, optional): printa o valor a ser retornado. Defaults to False.

    Returns:
        list: lista de sheets
    """
    if print_value:
        print(Workbook.sheetnames)
        return Workbook.sheetnames
    else:
        return Workbook.sheetnames

def len_columns(plan, print_value: bool=False) -> int:
    """Retorna a quantidade de colunas existentes na tabela

        pegue a planilha desse jeito:
        
        # nome da planilha (abre a planilha)
        ARQUIVO_EXCEL = openpyxl.load_workbook(os.path.abspath('ARQUIVO_EXCEL.xlsx'))
        
        nome_planilhas = ARQUIVO_EXCEL.sheetnames # saber quais são as planilhas que tem no arquivo excel
        print(nome_planilhas) # ['Página1']

        # pegar a sheet da planilha ARQUIVO_EXCEL
        PLANILHA = ARQUIVO_EXCEL['Página1']

    Args:
        plan (workbook): planilha
        print_value (bool, optional): Mostrar o valor retornado? Defaults to False.

    Returns:
        _type_: _description_
    """
    if print_value:
        print(plan.max_column)
        return plan.max_column
    else:
        return plan.max_column
    

def get_colun_data(plan, column: int, convert_tuple: bool=True, print_values: bool=True) -> list[str]:
    """Retorna os dados da coluna enviada, (tem que ser o indice da coluna)

        
        pegue a planilha desse jeito:
        
        # nome da planilha (abre a planilha)
        ARQUIVO_EXCEL = openpyxl.load_workbook(os.path.abspath('ARQUIVO_EXCEL.xlsx'))
        
        nome_planilhas = ARQUIVO_EXCEL.sheetnames # saber quais são as planilhas que tem no arquivo excel
        print(nome_planilhas) # ['Página1']

        # pegar a sheet da planilha ARQUIVO_EXCEL
        PLANILHA = ARQUIVO_EXCEL['Página1']
        
    Args:
        plan (planilha): planilha feita no openpyxl
        column (int): indice da coluna na tabela
        convert_tuple (bool): converte a lista de dados para tupla
    Returns:
        tuple or list: _description_
    """
    dados_da_coluna = []
    for linha in plan:
        if linha[column].value is not None:  # se o valor da planilha não for none
            cell = linha[column].value
            if cell is None:
                dados_da_coluna.append('None')
            else:
                dados_da_coluna.append(cell)
        else:
            dados_da_coluna.append('None')

    print(f'O nome da coluna é {dados_da_coluna[0]}')  # delete o nome da coluna
    del dados_da_coluna[0]  # deleta o nome da coluna
    if convert_tuple:
        dados_da_coluna = tuple(dados_da_coluna)
        
    if print_values:
        print(dados_da_coluna)
        return (dados_da_coluna)
    else:
        return (dados_da_coluna)


def return_columns_names(plan, len_columns: int, convert_to_tuple: bool=True, print_values :bool=True):
    nomes_das_colunas = []
    for coluna_index in range(len_columns):
        for linha in plan:
            coluna = linha[coluna_index].value
            nomes_das_colunas.append(coluna)
            break
    if convert_to_tuple:
        nomes_das_colunas = tuple(nomes_das_colunas)
    if print_values:
        print(nomes_das_colunas)
        return nomes_das_colunas
    else:
        return nomes_das_colunas