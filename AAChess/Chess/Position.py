
class Position:
    def __init__(self, row:int, column:int)->None:
        self.__row:int = row
        self.__column:int = column

    @property
    def row(self)->int:
        return self.__row
    @property
    def column(self)->int:
        return self.__column