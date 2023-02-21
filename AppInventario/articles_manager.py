""" Questo modulo contiene l'implementazione della classe ArticlesManager,
una classe che rappresenta una struttura dati.

Esempio:
    from articles_manager import ArticlesManager

    obj= ArticlesManager()
    obj.inser_val(record=('90515689','1000'))

    obj.rimoz_val(record=('90515689', '1000'))

    obj.modifica_val(record=('90515689', '500', '1000'))

    obj.insert_list_val([('90515689','1000'),('90515689','500'),('90515689','300')])    
"""

class ArticlesManager:
    ''' ArticlesManager e' una struttura dati che rappresenta il contenuto di un file inventario.

    La struttura dati organizza i valori in un dizionario nel seguente modo:
    - chiave (str): articolo 
    - valore (list): lista di str che rappresentano le quantita'

    Attributi:
        dict_articoli (dict): dizionario che contiene le varie letture di tuple (articolo, quantita')
    '''

    def __init__(self):
        '''Inizializza ArticlesManager'''

        self.dict_articoli = {}

    def inser_val(self, record: tuple) -> bool:
        """ Data una tupla, la inserisce in ArticlesManager

        Arg:
            record (tuple): tupla (articolo, quantita') da inserire

        Return:
            bool: True se operazione effettuata correttamente

        Esempio:
            >>> obj= ArticlesManager()
            >>> obj.inser_val(record=('90515689','1000'))
            True    
        """

        art,qty= record

        if art not in self.dict_articoli:
            self.dict_articoli[art]=[qty]
        else:
            self.dict_articoli[art].append(qty)

        return True

    def rimoz_val (self, record: tuple) -> bool:
        """ Data una tupla, rimuove la quantita' da ArticlesManager

        Arg:
            record (tuple): tupla (articolo, quantita') da rimuovere

        Return:
            bool: False se l'articolo non e' presente o se la quantita' non e' presente nell'articolo, altrimenti True 

        Esempio:
            >>> obj= ArticlesManager()
            >>> obj.inser_val(record=('90515689','1000'))
            >>> obj.rimoz_val(record=('90515689', '1000'))
            True            
        """

        art,qty= record

        if art not in self.dict_articoli:
            return False
        else:
            if qty not in self.dict_articoli[art]:
                return False
            else:
                pos = self.dict_articoli[art].index(qty)
                del self.dict_articoli[art][pos]
                return True

    def modifica_val(self, record:tuple) -> bool:
        """ Data una tupla, modifica una quantita' di un articolo gia' presente in ArticlesManager

        Arg:
            record (tuple): tupla (articolo, precedente_quantita', nuova_quantita')

        Return:
            bool: False se l'articolo non e' presente o se la precedente quantita' non e' presente nell'articolo, altrimenti True 

        Esempio:
            >>> obj= ArticlesManager()
            >>> obj.inser_val(record=('90515689','1000'))
            >>> obj.modifica_val(record=('90515689', '1000','500'))
            True
        """

        art,old_qty,new_qty= record

        if art not in self.dict_articoli:
            return False
        else:
            if old_qty not in self.dict_articoli[art]:
                return False
            else:
                pos = self.dict_articoli[art].index(old_qty)
                self.dict_articoli[art][pos]=new_qty
                return True

    def insert_list_val(self, lista_val: list) -> bool:
        '''Data una lista di tuple, inserisce tutti i valori in ArticlesManager
        
        Arg:
            lista_val(list): lista di tuple (articolo, quantita') da inserire 

        Return:
            bool: False se la lista e' vuota, altrimenti True

        Esempio:
            >>> obj= ArticlesManager()
            >>> obj.insert_list_val([('90515689','1000'),('90515689','500'),('90515689','300')])
            True            
        '''

        if not lista_val: #lista vuota
            return False

        for record in lista_val:
            self.inser_val(record)
        return True


