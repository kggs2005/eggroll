import copy

from .Move import Move
from .Tile import Tile, TileType


class GameState():
    '''
    Represents a moment within a game,
    including the grid at that moment,
    the moves they have made previously,
    the number of moves they have left,
    and the number of points the player has.
    GameStates are immutable.
    '''


    # Constructor
    def __init__(self, grid: list[list[Tile]], previous_moves: tuple[Move], remaining_moves: int, points: int):
        '''Constructs the necessary attributes for a game state.'''
        self.__grid = copy.deepcopy(grid)
        self.__previous_moves = previous_moves
        self.__remaining_moves = remaining_moves
        self.__points = points
    

    # Getters
    def get_grid(self) -> list[list[Tile]]:
        '''Returns a copy of the grid at this game state.'''
        return copy.deepcopy(self.__grid)
    

    def get_previous_moves(self) -> tuple[Move]:
        '''Returns a tuple of the previous moves before this game state.'''
        return self.__previous_moves
    

    def get_remaining_moves(self) -> int:
        '''Returns the number of remaining moves the player has left at this game state.'''
        return self.__remaining_moves
    

    def get_points(self) -> int:
        '''Returns the number of points the player currently has at this game state.'''
        return self.__points


    # Methods
    def grid_str(self) -> str:
        '''Returns the string representation of the grid.'''
        return '\n'.join(''.join(tile.emoji() for tile in row) for row in self.__grid)
    

    def previous_moves_str(self) -> str:
        '''Returns the string representation of the previous moves.'''
        return ''.join(move.arrow() for move in self.__previous_moves)
    
    
    def state_str(self) -> str:
        '''Returns the string representation of the game state.'''
        return '\n'.join((
            self.grid_str(),
            f'Previous moves: {self.previous_moves_str()}',
            f'Remaining moves: {self.__remaining_moves}',
            f'Points: {self.__points}'))
    

    def is_final(self) -> bool:
        '''Whether the game state is final (no moves left or no more live eggs).'''
        if self.__remaining_moves <= 0:
            return True
        return not any((tile.get_tile_type() == TileType.EGG for tile in row) for row in self.__grid)
    

    def find_all_coordinates(self, tile: TileType | str) -> tuple[tuple[int, int]]:
        '''
        Returns a tuple of tuples of the coordinates of all tiles of the given TileType.
        Can take a TileType or an emoji string as an argument.
        '''
        tile_type = tile if type(tile) == TileType else Tile(tile).get_tile_type()
        return tuple((i, j) for i in range(len(self.__grid)) for j in range(len(self.__grid[0])) if self.__grid[i][j].get_tile_type() == tile_type)
