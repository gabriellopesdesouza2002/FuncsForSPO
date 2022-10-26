"""
Funções de front-end para PySimpleGUI

"""

import os
import sys
import PySimpleGUI as sg
import winsound


########## For PySimpleGUI ########
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller 
    
        SE QUISER ADICIONAR ALGO NO ROBÔ BASTA USAR ESSA FUNÇÃO PARA ADICIONAR O CAMINHO PARA O EXECUTÁVEL COLOCAR
    """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
########## For PySimpleGUI ########


def popup_finalizado(text: str, title: str='Finalizado!', theme: str='Material1', autoclose: int=False, back_color: str='#E0E3E4', icon: str=False):
    winsound.MessageBeep()
    sg.theme(theme)
    if isinstance(icon, str): 
        sg.popup_ok(text,
                    title=title,
                    auto_close=autoclose,
                    background_color=back_color,
                    icon=resource_path(icon),
                    )
    else:
        sg.popup_ok(text,
                    title=title,
                    auto_close=autoclose,
                    background_color=back_color,
                    )
        

def popup_erro(text: str, title: str='Erro', theme: str='Material1', autoclose: int=False, back_color: str='#E0E3E4', icon: str=False):
    winsound.MessageBeep()

    sg.theme(theme)
    if isinstance(icon, str): 
        sg.popup_error(text,
                    title=title,
                    auto_close=autoclose,
                    background_color=back_color,
                    icon=resource_path(icon),
                    )
    else:
        sg.popup_error(text,
                    title=title,
                    auto_close=autoclose,
                    background_color=back_color,
                    )
        
def popup_pergunta(title: str, text: str, theme: str='Material1', autoclose: int=False, back_color: str='#E0E3E4', icon: str=False):
    winsound.MessageBeep()

    sg.theme(theme)
    if isinstance(icon, str): 
        return sg.popup_ok_cancel(text,
                    title=title,
                    auto_close=autoclose,
                    background_color=back_color,
                    icon=resource_path(icon),
                    )
    else:
        return sg.popup_ok_cancel(text,
                    title=title,
                    auto_close=autoclose,
                    background_color=back_color, 
                    )