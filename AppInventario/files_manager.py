""" Questo modulo contiene l'implementazione della classe FilesManager,
una classe che rappresenta una struttura dati.

Dipendenze:
    articles_manager (implementazione della classe ArticlesManager)  

Esempio:
    obj=FilesManager()
    obj.inser_file('inventario1')

    obj.rimoz_file('inventario1')

    obj.files['inventario1'].insert_list_val([('12567345','500'), ('67241568', '1000')])
    ret= obj.export_file('inventario1')

    obj.modifica_file_name('inventario1', 'inventario2')
"""

from articles_manager import ArticlesManager

class FilesManager:
    ''' FilesManager e' una struttura dati che rappresenta gli inventari di diverse zone in MP.

    La struttura dati organizza i valori in un dizionario nel seguente modo:
    - chiave (str): nome del file
    - valore (ArticlesManager): oggetto ArticlesManager che rappresenta il contenuto di un file inventario.

    Attributi:
        files (dict): dizionario che contiene i vari files inventario
    '''
    def __init__(self):
        '''Inizializza FilesManager'''

        self.files = {}

    def inser_file(self, file_name: str) -> bool:
        """ Dato un nome file, crea una nuova zona in FilesManager

        Arg:
            file_name (str): nome del file da inserire

        Return:
            bool: False se il nome del file e' gia' presente, altrimenti True

        Esempio:
            >>> obj=FilesManager()
            >>> obj.inser_file('inventario1')
            True
        """

        if file_name in self.files:
            return False
        
        self.files[file_name]= ArticlesManager()
        return True

    def rimoz_file (self, file_name: str) -> bool:
        """ Dato un nome file, elimina una zona in FilesManager

        Arg:
            file_name (str): nome del file da rimuovere

        Return:
            bool: False se il nome del file non e' presente, altrimenti True

        Esempio:
            >>> obj=FilesManager()
            >>> obj.inser_file('inventario1')
            >>> obj.rimoz_file('inventario1')
            True
        """

        if file_name not in self.files:
            return False
   
        del self.files[file_name]
        return True

    def export_file(self, file_name: str) -> list:
        """ Dato un nome file, esporta il contenuto in una lista

        Arg:
            file_name (str): nome del file da esportare

        Return:
            lista_articoli (list): lista vuota se il file non e' presente, altrimenti lista di tuple

        Esempio:
            >>> obj=FilesManager()
            >>> obj.inser_file('inventario1')
            >>> obj.files['inventario1'].insert_list_val([('12567345','500'), ('67241568', '1000')])
            >>> obj.export_file('inventario1')
            [('12567345','500'), ('67241568', '1000')]
        """

        if file_name not in self.files:
            return []
        
        lista_articoli=[]
        for articolo in self.files[file_name].dict_articoli:
            for qty in self.files[file_name].dict_articoli[articolo]:
                lista_articoli.append((articolo,qty))

        return lista_articoli

    def modifica_file_name(self, old_file_name: str, new_file_name : str) -> bool:
        """ Dato un nome file precedente e un nome file nuovo, rinomina una zona in FilesManager

        Arg:
            old_file_name (str): nome del file da rinominare
            new_file_name (str): nuovo nome del file 

        Return:
            bool: False se il nome del file precedente non e' presente o se il nuovo nome e' presente, altrimenti True

        Esempio:
            >>> obj=FilesManager()
            >>> obj.inser_file('inventario1')
            >>> obj.modifica_file_name('inventario1', 'inventario2')
            True
        """

        if old_file_name not in self.files:
            return False
        
        if new_file_name in self.files:
            return False

        self.files[new_file_name]= self.files[old_file_name]
        del self.files[old_file_name] 
        return True 

    def get_files(self) -> list:
        '''Ritorna la lista delle chiavi del dizionario contenuto in FilesManager

        Return:
            (list): lista delle chiavi del dizionario 

        Esempio:
            >>> obj=FilesManager()
            >>> obj.get_files()
            ['inventario1', 'inventario2']
        '''

        return list(self.files.keys())







