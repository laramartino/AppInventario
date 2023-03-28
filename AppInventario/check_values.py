"""This module contains the implementation of functions that check the values of article, new article and quantity inserted by user.

Dependencies:
    pandas: library for manipulating data in Excel files.   
"""

import pandas as pd

def check_art(art: str) -> bool:
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
        False if the string length is not 8, if there are letters other than those mentioned above or if the article is not in MP registry,
        otherwise True.
        
    Example:
        from check_values import check_art

        print(check_art('90351051'))   
        print(check_art('H0351051'))
    """

    if len(art) != 8:
        return False
    
    for a in art:
        if a not in 'ZKHBSN012345679': 
            return False

    excel_file = pd.read_excel('C:\\Users\\Lara\\source\\repos\\laramartino\\AppInventario\\AppInventario\\anagrafica_articoli.xlsx') #Read file Excel.

    series_articles_mp = pd.Series(excel_file['ARTICOLO']) #One-dimensional ndarray with row index.
    
    articles_mp = series_articles_mp.to_string(index = False) #Represent the data of the Series as str.

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
        if not 48 <= ord(q) <= 57: #48 = '0', 57 = '9'.
            return False
    return True

def check_new_art(new_art: str) -> bool:
    """Check the value of the new article inserted by user.

    Accepted letters are only: 
    Z (zinc-coated article)
    K (SKF customer)
    H (Parker customer) 
    B (tempered processing) 
    S (article without hole)
    N (article without logo)

    Arg:
        art (str): new article string.

    Return:
        False if the string length is not 8, if there are letters other than those mentioned above or if the article is already in the MP registry,
        otherwise True.
        
    Example:
        from check_values import check_new_art

        print(check_art('Z9035105'))   
        print(check_art('01111111'))
    """

    if len(new_art) != 8:
        return False
    
    for a in new_art:
        if a not in 'ZKHBSN0123456789':
            return False

    #Read Excel file and get the 'ARTICOLO' column as a list of str.
    articles_mp_list = pd.read_excel('C:\\Users\\Lara\\source\\repos\\laramartino\\AppInventario\\AppInventario\\anagrafica_articoli.xlsx')['ARTICOLO'].tolist() 

    if new_art in articles_mp_list:
        return False

    return True
