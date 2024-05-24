import unittest
from .Position import Position
from .Pawn import Pawn
from .Rook import Rook
from .Bishop import Bishop
from .Knight import Knight
from .Queen import Queen
from .King import King


class Test(unittest.TestCase):

    def test_pawn3(self):
        piece = Pawn("black", "pawn", 0)
        start = Position(1,0)
        end = Position(3,2)
        self.assertFalse(piece.can_move(start, end))
    
    def test_rook1(self):
        piece = Rook("white", "rook", 0)
        start = Position(0,0)
        end = Position(4,0)
        self.assertTrue(piece.can_move(start, end))
        
    def test_rook2(self):
        piece = Rook("white", "rook", 0)
        start = Position(4,6)
        end = Position(4,1)
        self.assertTrue(piece.can_move(start, end))
        
    def test_rook3(self):
        piece = Rook("white", "rook", 1)
        start = Position(0,0)
        end = Position(0,0)
        self.assertFalse(piece.can_move(start, end))
        
    def test_rook4(self):
        piece = Rook("white", "rook", 1)
        start = Position(4,5)
        end = Position(6,7)
        self.assertFalse(piece.can_move(start, end))
        
    def test_knight1(self):
        piece = Knight("white", "knight",0)
        start = Position(0,0)
        end = Position(0,0)
        self.assertFalse(piece.can_move(start, end))
        
    def test_knight2(self):
        piece = Knight("black", "knight",0)
        start = Position(2,5)
        end = Position(4,6)
        self.assertTrue(piece.can_move(start, end))
        
    def test_knight3(self):
        piece = Knight("black", "knight",0)
        start = Position(2,5)
        end = Position(4,7)
        self.assertFalse(piece.can_move(start, end))
        
    def test_knight4(self):
        piece = Knight("black", "knight",1)
        print(piece.code())
        start = Position(2,5)
        end = Position(4,7)
        self.assertFalse(piece.can_move(start, end)) 
    
    def test_bishop1(self):
        piece = Bishop("black", "bishop",0)
        print(piece.code())
        start = Position(2,5)
        end = Position(4,7)
        self.assertTrue(piece.can_move(start, end)) 
        
    def test_bishop2(self):
        piece = Bishop("white", "bishop",0)
        print(piece.code())
        start = Position(0,2)
        end = Position(2,0)
        self.assertTrue(piece.can_move(start, end)) 
        
    def test_bishop3(self):
        piece = Bishop("white", "bishop",0)
        print(piece.code())
        start = Position(4,1)
        end = Position(4,3)
        self.assertFalse(piece.can_move(start, end)) 
        
    def test_queen1(self):
        piece = Queen("white", "queen",0)
        start = Position(0, 3)
        end = Position(3, 3)
        self.assertTrue(piece.can_move(start, end))

    def test_queen2(self):
        piece = Queen("black", "queen",0)
        start = Position(7, 4)
        end = Position(5, 6)
        self.assertTrue(piece.can_move(start, end))

    def test_king1(self):
        piece = King("white", "king",0)
        start = Position(0, 4)
        end = Position(1, 3)
        self.assertTrue(piece.can_move(start, end))

    def test_king2(self):
        piece = King("black", "king",0)
        start = Position(7, 4)
        end = Position(6, 3)
        self.assertTrue(piece.can_move(start, end))
        
    def test_pawn1(self):
        piece = Pawn("white", "pawn", 0)
        start = Position(1, 4)
        end = Position(3, 4)
        self.assertTrue(piece.can_move(start, end))
        
    def test_pawn2(self):
        piece = Pawn("black", "pawn", 0)
        start = Position(5, 4)
        end = Position(6, 5)
        self.assertFalse(piece.can_move(start, end))
                
    
    
if __name__ == '__main__':
    unittest.main()