"""Questo modulo contiene l'implementazione di funzioni che controllano i valori di articolo e quantita' inseriti dall'utente

Dipendenze:
    pandas: libreria per la manipolazione dati in file Excel    
"""

import pandas as pd

def check_art(art:str) -> bool:
    """Controlla il valore dell'articolo inserito dall'utente.

    Le lettere accettate sono solamente: 
    Z (prodotto zincato)
    K (cliente SKF)
    H (cliente Parker) 
    B (lavorazione di bonifica) 
    S (prodotto senza foro)
    N (assenza del logo sul prodotto)

    Arg:
        art (str): stringa dell'articolo.

    Return:
        False se la stringa ha una lunghezza diversa da 8, vi sono lettere diverse da quelle sopra citate o non e' presente nel catalogo MP, 
        altrimenti True.
        
    Esempio:
        from check_valori import check_art

        print(check_art('90351051'))   
        print(check_art('H0351051'))
    """

    if len(art) != 8:
        return False
    
    for a in art:
        if 65 <= ord(a) <= 90 and a not in 'ZKHBSN': #65= 'A', 90='Z'.
            return False

    file_excel = pd.read_excel('anagrafica_articoli.xls') #lettura file Excel.

    series_articoli_mp = pd.Series(file_excel['ARTICOLO']) #ndarray unidimensionale con indici di riga.
    
    articoli_mp = series_articoli_mp.to_string(index = False) #rappresentazione dei dati della Series come str.

    if art not in articoli_mp:
        return False

    return True

def check_qty(qty:str) -> bool:
    """Controlla il valore della quantita' inserita dall'utente.

    Arg:
        qty (str): stringa della quantita'.

    Return:
        False se il valore inserito e' nullo, se e' un numero decimale o negativo, altrimenti True.

    Esempio:
        from check_valori import check_qty

        print(check_qty('1000'))
    """

    if qty == '':
       return False
    for q in qty:
        if not 48 <= ord(q) <= 57: #48='0', 57='9'.
            return False
    return True