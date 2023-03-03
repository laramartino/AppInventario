"""Questo modulo contiene l'implementazione della classe FilesManager,
una classe che rappresenta una struttura dati.

Dipendenze:
    articles_manager (implementazione della classe ArticlesManager)  

Esempio:
    from files_manager import FilesManager

    obj = FilesManager()
    obj.insert_file('inventario1')

    obj.delete_file('inventario1')

    obj.files['inventario1'].insert_records_list([('12567345','500'), ('67241568', '1000')])
    ret = obj.export_file('inventario1')
"""

from articles_manager import ArticlesManager

class FilesManager:
    """FilesManager e' una struttura dati che rappresenta gli inventari di diverse zone in MP.

    La struttura dati organizza i valori in un dizionario nel seguente modo:
    - chiave (str): nome del file.
    - valore (ArticlesManager): oggetto ArticlesManager che rappresenta il contenuto di un file inventario.

    Attributi:
        files (dict): dizionario che contiene i vari files inventario.
    """

    def __init__(self):
        """Inizializza FilesManager."""

        self.files = {}

    def insert_file(self, file_name: str) -> bool:
        """Dato un nome file, crea una nuova zona in FilesManager.

        Arg:
            file_name (str): nome del file da inserire.

        Return:
            bool: False se il nome del file e' gia' presente, altrimenti True.

        Esempio:
            >>> obj = FilesManager()
            >>> obj.insert_file('inventario1')
            True
        """

        if file_name in self.files:
            return False
        
        self.files[file_name] = ArticlesManager()
        return True

    def delete_file (self, file_name: str) -> bool:
        """Dato un nome file esistente, elimina una zona in FilesManager.

        Arg:
            file_name (str): nome del file da rimuovere.

        Return:
            bool: False se il nome del file non e' presente, altrimenti True.

        Esempio:
            >>> obj = FilesManager()
            >>> obj.insert_file('inventario1')
            >>> obj.delete_file('inventario1')
            True
        """

        if file_name not in self.files:
            return False
   
        del self.files[file_name]
        return True

    def export_file(self, file_name: str) -> list:
        """Dato un nome file esistente, esporta il contenuto in una lista di tuple.

        Arg:
            file_name (str): nome del file da esportare.

        Return:
            lista_articoli (list): lista vuota se il file non e' presente, altrimenti lista di tuple.

        Esempio:
            >>> obj = FilesManager()
            >>> obj.insert_file('inventario1')
            >>> obj.files['inventario1'].insert_records_list([('12567345','500'), ('67241568', '1000')])
            >>> obj.export_file('inventario1')
            [('12567345','500'), ('67241568', '1000')]
        """

        if file_name not in self.files:
            return []
        
        lista_articoli = []
        for articolo in self.files[file_name].dict_articoli: #percorso che indica ArticlesManager del file da esportare.
            for qty in self.files[file_name].dict_articoli[articolo]: #percorso che indica la lista delle qty di un articolo del file da esportare.
                lista_articoli.append((articolo,qty))

        return lista_articoli 

    def get_files(self) -> list:
        """Ritorna la lista delle chiavi del dizionario contenuto in FilesManager.

        Return:
            (list): lista delle chiavi del dizionario 

        Esempio:
            >>> obj = FilesManager()
            >>> obj.get_files()
            ['inventario1', 'inventario2']
        """

        return list(self.files.keys())