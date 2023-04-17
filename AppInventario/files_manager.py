"""This module contains the FilesManager implementation, a class representing a data structure.

Dependencies:
    articles_manager: ArticlesManager implementation.  

Example:
    from files_manager import FilesManager

    obj = FilesManager()
    obj.insert_file('inventario1')

    obj.delete_file('inventario1')

    obj.files['inventario1'].insert_records_list([('12567345','500'), ('67241568', '1000')])
    ret = obj.export_file('inventario1')
"""

from articles_manager import ArticlesManager

class FilesManager:
    """FilesManager is the data structure representing the inventories of different areas in MP.

    The data structure is a dictionary organized as follows:
    - key (str): filename
    - value (ArticlesManager): ArticlesManager object representing the content of an inventory file.

    Attributes:
        files (dict): dictionary containing the different inventory files.
    """

    def __init__(self):
        """Initialize FilesManager."""

        self.files = {}

    def insert_file(self, file_name: str) -> bool:
        """Inserted a filename, create a new key in FilesManager.

        Arg:
            file_name (str): filename to add.

        Return:
            bool: False if the filename already exists, otherwise True.

        Example:
            >>> obj = FilesManager()
            >>> obj.insert_file('inventario1')
            True
        """

        if file_name in self.files:
            return False
        
        self.files[file_name] = ArticlesManager()
        return True

    def delete_file (self, file_name: str) -> bool:
        """Inserted an existing filename, the related key is deleted from FilesManager.

        Arg:
            file_name (str): filename to delete.

        Return:
            bool: False if the filename doesn't exist in FilesManager, otherwise True.

        Example:
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
        """Inserted an existing filename, the content is exported in a list of tuples.

        Arg:
            file_name (str): filename to export.

        Return:
            lista_articoli (list): empty list if the file doesn't exist, otherwise a list of tuples.

        Example:
            >>> obj = FilesManager()
            >>> obj.insert_file('inventario1')
            >>> obj.files['inventario1'].insert_records_list([('12567345','500'), ('67241568', '1000')])
            >>> obj.export_file('inventario1')
            [('12567345','500'), ('67241568', '1000')]
        """

        if file_name not in self.files:
            return []
        
        lista_articoli = []
        for articolo in self.files[file_name].dict_articoli:  # Path indicating ArticlesManager of the file to export.
            for qty in self.files[file_name].dict_articoli[articolo]:  # Path indicating qty list of an article in the file to export.
                lista_articoli.append((articolo,qty))

        return lista_articoli 

    def get_files(self) -> list:
        """Return the list of the dictionary keys contained in FilesManager.

        Return:
            (list): list of the dictionary keys. 

        Example:
            >>> obj = FilesManager()
            >>> obj.get_files()
            ['inventario1', 'inventario2']
        """

        return list(self.files.keys())

