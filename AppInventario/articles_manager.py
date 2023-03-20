"""This module contains the ArticlesManager implementation, a class representing a data structure.

Example:
    from articles_manager import ArticlesManager

    obj = ArticlesManager()
    obj.insert_record(record = ('90515689','1000'))

    obj.delete_record(record = ('90515689', '1000'))

    obj.modify_record(record = ('90515689', '500', '1000'))

    obj.insert_records_list([('90515689','1000'),('90515689','500'),('90515689','300')])    
"""

class ArticlesManager:
    """ArticlesManager is the data structure representing the content of an inventory file.

    The data structure is a dictionary organized as follows:
    - key (str): article.
    - value (list): list of quantities as string.

    Attributes:
        dict_articoli (dict): dictionary containing tuples (article, quantity).
    """

    def __init__(self):
        """Initialize ArticlesManager."""

        self.dict_articoli = {}

    def insert_record(self, record: tuple) -> bool:
        """Given a tuple, insert the record into ArticlesManager.

        If the article is not present in the keys, create a new key-value pair.

        Arg:
            record (tuple): tuple (article, quantity) to insert.

        Return:
            bool: True if succesful.

        Example:
            >>> obj = ArticlesManager()
            >>> obj.insert_record(record = ('90515689','1000'))
            True    
        """

        art, qty = record

        if art not in self.dict_articoli:
            self.dict_articoli[art] = [qty]
        else:
            self.dict_articoli[art].append(qty)

        return True

    def delete_qty(self, record: tuple) -> bool:
        """Given a tuple, delete the quantity of record from ArticlesManager.

        If there are not quantities for an article, the method does not delete the article, but it has an empty list.

        Arg:
            record (tuple): tuple (article, quantity) with quantity to delete.

        Return:
            bool: False if the article is not in ArticlesManager or if the quantity is not present in the article, otherwise True.

        Example:
            >>> obj = ArticlesManager()
            >>> obj.insert_record(record = ('90515689','1000'))
            >>> obj.delete_record(record = ('90515689', '1000'))
            True            
        """

        art, qty = record

        if art not in self.dict_articoli:
            return False
        else:
            if qty not in self.dict_articoli[art]:
                return False
            else:
                pos = self.dict_articoli[art].index(qty)
                del self.dict_articoli[art][pos]
                return True

    def modify_record(self, record: tuple) -> bool:
        """Given a tuple, modify a quantity of an article in ArticleManager.

        Arg:
            record (tuple): tuple (article, old_quantity, new_quantity).

        Return:
            bool: False if the article is not in ArticlesManager or if the old_quantity is not present in the article, otherwise True.

        Example:
            >>> obj = ArticlesManager()
            >>> obj.insert_record(record = ('90515689','1000'))
            >>> obj.modify_record(record = ('90515689', '1000','500'))
            True
        """

        art, old_qty, new_qty = record

        if art not in self.dict_articoli:
            return False
        else:
            if old_qty not in self.dict_articoli[art]:
                return False
            else:
                pos = self.dict_articoli[art].index(old_qty)
                self.dict_articoli[art][pos] = new_qty
                return True

    def insert_records_list(self, lista_val: list) -> bool:
        """Given a list of tuples, insert all records in ArticlesManager.
        
        Arg:
            lista_val (list): list of tuples (article, quantity) to insert.

        Return:
            bool: False if the list is empty, otherwise True.

        Example:
            >>> obj = ArticlesManager()
            >>> obj.insert_records_list([('90515689','1000'),('90515689','500'),('90515689','300')])
            True            
        """

        if not lista_val: #empty list.
            return False

        for record in lista_val:
            self.insert_record(record)
        return True


