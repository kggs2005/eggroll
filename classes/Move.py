from enum import Enum


class MoveType(Enum):
    '''UP | DOWN | LEFT | RIGHT'''
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Move:
    '''
    Represents a move that a player can make.
    There are 4 types of moves: up, down, left, or right.
    '''


    # Constructor
    def __init__(self, move_type: MoveType | str):
        '''
        Constructs and initializes a Move.
        Can take a MoveType or an arrow string as an argument for the constructor.
        '''
        if isinstance(move_type, MoveType):
            self.__move_type = move_type
        elif isinstance(move_type, str):
            if move_type == '↑':
                self.__move_type == MoveType.UP
            elif move_type == '↓':
                self.__move_type == MoveType.DOWN
            elif move_type == '←':
                self.__move_type == MoveType.LEFT
            elif move_type == '→':
                self.__move_type == MoveType.RIGHT
            else:
                raise ValueError(f'Expected arrow character as argument. Instead got {move_type}')
        else:
            raise TypeError(f'Expected MoveType or string as an argument. Instead got {type(move_type).__name__}')
  

    # Getters
    def get_type(self) -> MoveType:
        '''Returns the type of move.'''
        return self.__move_type
        

    # Methods
    def arrow(self) -> str:
        '''Returns the corresponding arrow of the move direction as a string.'''
        if self.__move_type == MoveType.UP:
            return '↑'
        elif self.__move_type == MoveType.DOWN:
            return '↓'
        elif self.__move_type == MoveType.LEFT:
            return '←'
        elif self.__move_type == MoveType.RIGHT:
            return '→'
