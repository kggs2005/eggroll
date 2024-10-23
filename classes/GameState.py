import copy

from .Move import Move, MoveType
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
        lines: tuple[str] = (
            self.grid_str(),
            f'Previous moves: {self.previous_moves_str()}',
            f'Remaining moves: {self.__remaining_moves}',
            f'Points: {self.__points}')
        
        if self.eggs_are_rolling():
            lines = (*lines, f'Performing move: {self.get_previous_moves()[-1].arrow()}')

        return '\n'.join(lines)
    

    def is_final(self) -> bool:
        '''
        Whether the game state is final.
        Returns True if either
        1) there are no eggs left, or
        2) eggs are not rolling and there are no moves left.
        '''
        return len(self.find_all_coordinates(TileType.EGG)) == 0 or (not self.eggs_are_rolling() and self.__remaining_moves <= 0)

                    
    def find_all_coordinates(self, tile: TileType | str) -> tuple[tuple[int, int]]:
        '''
        Returns a tuple of tuples of the coordinates of all tiles of the given TileType.
        Can take a TileType or an emoji string as an argument.
        '''
        tile_type = tile if type(tile) == TileType else Tile(tile).get_tile_type()
        return tuple((i, j) for i in range(len(self.__grid)) for j in range(len(self.__grid[0])) if self.__grid[i][j].get_tile_type() == tile_type)


    def eggs_are_rolling(self) -> bool:
        '''Whether the eggs are still rolling. Returns False if there are no eggs.'''
        # Game just started. Eggs are not rolling.
        if len(self.__previous_moves) == 0:
            return False

        # Make references to the previous move
        previous_move = self.__previous_moves[-1]

        # Find all eggs and check if any egg has a grass, empty nest, or frying pan one tile in the previous move's direction.
        egg_coordinates = self.find_all_coordinates(TileType.EGG)

        for (i, j) in egg_coordinates:
            # Reference tile (tile to check) depends on previous move's direction.
            # All level grids have walls in the outer layer, so there shouldn't be any index errors since eggs will always have tiles adjacent to them.
            ref_tile: TileType = None
            if previous_move.get_type() == MoveType.UP:
                tile_above = self.__grid[i - 1][j].get_tile_type()
                ref_tile = tile_above
            elif previous_move.get_type() == MoveType.DOWN:
                tile_below = self.__grid[i + 1][j].get_tile_type()
                ref_tile = tile_below
            elif previous_move.get_type() == MoveType.LEFT:
                tile_left = self.__grid[i][j - 1].get_tile_type()
                ref_tile = tile_left
            elif previous_move.get_type() == MoveType.RIGHT:
                tile_right = self.__grid[i][j + 1].get_tile_type()
                ref_tile = tile_right
            
            # Check if the reference tile is a grass, empty nest, or frying pan.
            if ref_tile in (TileType.GRASS, TileType.EMPTY_NEST, TileType.FRYING_PAN):
                return True
        
        # Could not find any egg with a grass, empty nest, or frying pan one tile in the previous move's direction, or could not find any eggs.
        return False
        