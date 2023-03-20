"""This module contains the implementation of functions that check the values of article and quantity inserted by user.

Dependencies:
    pandas: library for manipulating data in Excel files.   
"""

import pandas as pd

def check_art(art:str) -> bool:
    """Check the value of the article inserted by user.

    Accepted letters are only: 
    Z (zinc-coated article)
    K (SKF customer)
    H (Parker customer) 
    B (tempered processing) 
    S (article without hole)
    N (article without logo)

    Arg:
        art (str): article string.

    Return:
        False if the string length is not 8, if there are letters other than those mentioned above or if the article is not in MP catalogue,
        otherwise True.
        
    Example:
        from check_valori import check_art

        print(check_art('90351051'))   
        print(check_art('H0351051'))
    """

    if len(art) != 8:
        return False
    
    for a in art:
        if 65 <= ord(a) <= 90 and a not in 'ZKHBSN': #65 = 'A', 90 = 'Z'.
            return False

    excel_file = pd.read_excel('anagrafica_articoli.xls') #read file Excel.

    series_articles_mp = pd.Series(excel_file['ARTICOLO']) #one-dimensional ndarray with row index.
    
    articles_mp = series_articles_mp.to_string(index = False) #represent the data of the Series as str.

    if art not in articles_mp:
        return False

    return True

def check_qty(qty:str) -> bool:
    """Check the value of the quantity inserted by user.

    Arg:
        qty (str): quantity string.

    Return:
        False if the inserted value is null, a decimal or negative number, otherwise True.

    Example:
        from check_valori import check_qty

        print(check_qty('1000'))
    """

    if qty == '':
       return False
    for q in qty:
        if not 48 <= ord(q) <= 57: #48 = '0', 57 = '9'.
            return False
    return True


