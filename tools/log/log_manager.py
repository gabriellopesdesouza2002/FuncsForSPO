import logging
import os

path_logs_dir = os.path.abspath(r'.\logs')
path_logs_file = os.path.abspath(r'.\logs\botLog.log')


def limpa_logs():
    if os.path.exists(path_logs_dir):
        try:
            os.remove(path_logs_file)
        except Exception:
            ...
    else:
        os.mkdir(path_logs_dir)


def faz_log(msg: str, level: str = 'i'):
    """Faz log na pasta padrão (./logs/botLog.log)

    Args:
        msg (str): "Mensagem de Log"
        level (str): "Niveis de Log"
        
        Levels:
            'i' or not passed = info and print

            'i*' = info log only

            'w' = warning
            
            'c*' = critical / Exception Error exc_info=True
            
            'c' = critical
            
            'e' = error
    """
    path_logs_dir = os.path.abspath(r'.\logs')
    path_logs_file = os.path.abspath(r'.\logs\botLog.log')

    if not os.path.exists(path_logs_dir):
        os.mkdir(path_logs_dir)
    else:
        ...

    if isinstance(msg, (str)):
        pass
    else:
        print('COLOQUE UMA STING NO PARAMETRO MSG!')

    if isinstance(level, (str)):
        pass
    else:
        print('COLOQUE UMA STING NO PARAMETRO LEVEL!')

    if isinstance(msg, (str)) and isinstance(level, (str)):
        if level == 'i' or level == '' or level is None:
            logging.basicConfig(filename=path_logs_file,
                                encoding='utf-8',
                                filemode='w',
                                format='%(asctime)s - %(levelname)s - %(message)s',
                                level=logging.INFO
                                )
            print(msg)
            if r'\n' in msg:
                msg = msg.replace(r"\n", "")
            logging.info(msg)

        if level == 'i*':
            logging.basicConfig(filename=path_logs_file,
                                encoding='utf-8',
                                filemode='w',
                                format='%(asctime)s - %(levelname)s - %(message)s',
                                level=logging.INFO
                                )
            if r'\n' in msg:
                msg = msg.replace(r"\n", "")
            logging.info(msg)

        elif level == 'w':
            logging.basicConfig(filename=path_logs_file,
                                encoding='utf-8',
                                filemode='w',
                                format='%(asctime)s - %(levelname)s - %(message)s',
                                level=logging.WARNING
                                )
            logging.warning(msg)
            print('! ' + msg + ' !')

        elif level == 'e':
            logging.basicConfig(filename=path_logs_file,
                                encoding='utf-8',
                                filemode='w',
                                format='%(asctime)s - %(levelname)s - %(message)s',
                                level=logging.ERROR
                                )
            logging.error(msg)
            print('!! ' + msg + ' !!')

        elif level == 'c':
            logging.basicConfig(filename=path_logs_file,
                                encoding='utf-8',
                                filemode='w',
                                format='%(asctime)s - %(levelname)s - %(message)s',
                                level=logging.CRITICAL
                                )
            logging.critical(msg)
            print('!!! ' + msg + ' !!!')

        elif level == 'c*':
            logging.basicConfig(filename=path_logs_file,
                                encoding='utf-8',
                                filemode='w',
                                format='%(asctime)s - %(levelname)s - %(message)s',
                                level=logging.CRITICAL
                                )
            logging.critical(msg, exc_info=True)
            print('!!! ' + msg + ' !!!')


if __name__ == '__main__':
    faz_log('ass')
    limpa_logs()
