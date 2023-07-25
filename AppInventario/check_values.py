"""This module contains the implementation of functions that check the values of article, new article and quantity inserted by user.

There is also the function that shows touch keyboard.

Dependencies:
    pandas: library for manipulating data in Excel files.   
    subprocess: module that allows to generate new processes, connect to their input/output/error tubes and get their return codes.
"""

import pandas as pd
import subprocess

def show_keyboard(event):
    """Show touch keyboard."""

    subprocess.Popen(['C:\\PROGRA~1\\COMMON~1\\MICROS~1\\ink\\TabTip.exe'], shell=True)

def check_art(art: str) -> bool:
    """Check the value of the article inserted by user.

    Arg:
        art (str): article string.

    Return:
        False if the string length is not 8, if there are no capital letters and/or numbers or if the article is not in MP registry,
        otherwise True.
        
    Example:
        from check_values import check_art

        print(check_art('90351051'))   
        print(check_art('H0351051'))
    """

    if len(art) != 8:
        return False
    
    for a in art:
        if a not in 'QWERTYUIOPASDFGHJKLZXCVBNM0123456789': 
            return False

    excel_file = pd.read_excel('C:\\Users\\lara_\\OneDrive\\Desktop\\AppInventario\\AppInventario\\anagrafica_articoli.xlsx')
    series_articles_mp = pd.Series(excel_file['ARTICOLO'])    
    articles_mp = series_articles_mp.to_string(index=False)  # Represent the data of the Series as str.

    if art not in articles_mp:
        return False

    return True

def check_qty(qty: str) -> bool:
    """Check the value of the quantity inserted by user.

    Arg:
        qty (str): quantity string.

    Return:
        False if the inserted value is null, a decimal or negative number, otherwise True.

    Example:
        from check_values import check_qty

        print(check_qty('1000'))
    """

    if qty == '':
       return False
    for q in qty:
        if not 48 <= ord(q) <= 57:  # 48 = '0', 57 = '9'.
            return False
    return True

def check_new_art(new_art: str) -> bool:
    """Check the value of the new article inserted by user.

    Arg:
        art (str): new article string.

    Return:
        False if the string length is not 8, if there are no capital letters and/or numbers or if the article is already in the MP registry,
        otherwise True.
        
    Example:
        from check_values import check_new_art

        print(check_new_art('Z9035105'))   
        print(check_new_art('01111111'))
    """

    if len(new_art) != 8:
        return False
    
    for a in new_art:
        if a not in 'QWERTYUIOPASDFGHJKLZXCVBNM0123456789':
            return False

    excel_file = pd.read_excel('C:\\Users\\lara_\\OneDrive\\Desktop\\AppInventario\\AppInventario\\anagrafica_articoli.xlsx')  
    series_articles_mp = pd.Series(excel_file['ARTICOLO']) 
    articles_mp = series_articles_mp.to_string(index=False)  

    if new_art in articles_mp:
        return False

    return True
