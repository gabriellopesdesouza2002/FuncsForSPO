from ftplib import FTP_TLS
import ftplib


def enviar_arquivo_via_ftp(host: str, user: str, passwd: str, filename_path_ftp: str, filename_path_upload: str):
    """Envia um arquivo via FTP
    ### Só é possível enviar arquivos, e um de cada vez.

    Args:
        host (str): Host do FTP
        user (str): Usuário do FTP
        passwd (str): Senha do FTP
        filename_path_ftp (str): Caminho do arquivo no FTP
        filename_path_upload (str): Caminho do arquivo no Computador
    """
    with FTP_TLS(host=host, user=user, passwd=passwd) as ftp:
        print('Acessando FTP_TLS')
        with open(filename_path_upload, "rb") as file:
            # use FTP's STOR command to upload the file
            ftp.storbinary(f"STOR {filename_path_ftp}", file)
            print('Upload concluido!')
            
            
def baixar_arquivo_via_ftp(host: str, user: str, passwd: str, filename_path_ftp: str, filename_path_download: str) -> None:
    """Faz o download de um arquivo via FTP

    Args:
        host (str): Host do FTP
        user (str): Usuário do FTP
        passwd (str): Senha do FTP
        filename_path_ftp (str): Caminho do arquivo para baixar (PATH FTP)
        filename_path_download (str): Caminho do Download
    """
    with FTP_TLS(host=host, user=user, passwd=passwd) as ftp:
        print('Acessando FTP_TLS')
        with open(filename_path_download, "wb") as file_:
            print('Fazendo download do arquivo...')
            ftp.retrbinary(f"RETR {filename_path_ftp}", file_.write,)
            print('Download concluido!')
            
            
def alterar_permissao_de_arquivo_ftp(host: str, user: str, passwd: str, file_path_ftp: str, permission: str|int, force_permission: bool=False):
    """Altera a permissão em um arquivo ou pasta em um servidor FTP
    
    Permissões Disponiveis:
    
    #### 700
        Owner -> Ler; Gravar e Executar
        
        Group -> NOT ler; NOT gravar and NOT Executar
        
        Public -> NOT ler; NOT gravar and NOT Executar
        
    #### 770
        Owner -> Ler; Gravar e Executar
        
        Group -> Ler; Gravar e Executar
        
        Public -> NOT ler; NOT gravar and NOT Executar
        
    #### 777
        Owner -> Ler; Gravar e Executar
        
        Group -> Ler; Gravar e Executar
        
        Public -> Ler; Gravar e Executar
        
    #### 000
        Owner -> NOT ler; NOT gravar and NOT Executar
        
        Group -> NOT ler; NOT gravar and NOT Executar
        
        Public -> NOT ler; NOT gravar and NOT Executar

    Args:
        host (str): host ftp
        user (str): user ftp
        passwd (str): password ftp
        file_path_ftp (str): path_archive_ftp
        permission (str|int): permission
        force_permission (bool|int): force permission not predefined
    """
    with FTP_TLS(host=host, user=user, passwd=passwd) as ftp:
        print('Acessando FTP_TLS')
        try:
            if permission == '700' or permission == 700:
                ftp.sendcmd('SITE CHMOD 700 ' + file_path_ftp)
                print('Permissão 700 alterada com sucesso...')
                
            elif permission == '770' or permission == 770:
                ftp.sendcmd('SITE CHMOD 770 ' + file_path_ftp)
                print('Permissão 770 alterada com sucesso...')
                
            elif permission == '777' or permission == 777:
                ftp.sendcmd('SITE CHMOD 777 ' + file_path_ftp)
                print('Permissão 777 alterada com sucesso...')
            
            else:
                if force_permission:
                    print('Permissão não reconhecida...')
                else:
                    print('Permissão não reconhecida...\nNão haverá mudança forçada, para isso ative o parâmetro force_permission')
                
        except ftplib.error_perm as e:
            e = str(e)
            if 'No such file or directory' in e:
                print(f'Diretório ou arquivo não encontrado no servidor -> {file_path_ftp}')