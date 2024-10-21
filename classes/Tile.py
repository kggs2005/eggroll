from enum import Enum


class TileType(Enum):
    '''WALL | GRASS | EGG | EMPTY_NEST | FULL_NEST | FRYING_PAN'''
    WALL = 0
    GRASS = 1
    EGG = 2
    EMPTY_NEST = 3
    FULL_NEST = 4
    FRYING_PAN = 5


class Tile:
    '''
    Represents a tile in the game's grid.
    A tile can be a wall, a tile of grass, an egg, an empty nest, a full nest, or a frying pan.
    '''


    # Constructor
    def __init__(self, tile_type: TileType | str):
        '''
        Constructs and initializes a Tile.
        Can take a TileType or an emoji string as an argument for the constructor.
        '''
        if isinstance(tile_type, TileType):
            self.__tile_type = tile_type
        elif isinstance(tile_type, str):
            if tile_type == '🧱':
                self.__tile_type = TileType.WALL
            elif tile_type == '🟩':
                self.__tile_type = TileType.GRASS
            elif tile_type == '🥚':
                self.__tile_type = TileType.EGG
            elif tile_type == '🐥':
                self.__tile_type = TileType.EMPTY_NEST
            elif tile_type == '🐣':
                self.__tile_type = TileType.FULL_NEST
            elif tile_type == '🍳':
                self.__tile_type = TileType.FRYING_PAN
            else:
                raise ValueError(f'Expected tile emoji as argument. Instead got {tile_type}')
        else:
            raise TypeError(f'Expected TileType or string as an argument. Instead got {type(tile_type).__name__}')

    
    # Getters
    def get_tile_type(self) -> TileType:
        '''Returns the type of the tile'''
        return self.__tile_type
    

    # Setters
    def set_tile_type(self, tile_type: TileType | str) -> None:
        '''
        Changes the type of the tile.
        Can accept TileType or emoji string as an argument.
        '''
        if isinstance(tile_type, TileType):
            self.__tile_type = tile_type
        elif isinstance(tile_type, str):
            self.__tile_type = Tile(str).get_tile_type()
        else:
            raise TypeError(f'Expected TileType or string as an argument. Instead got {type(tile_type).__name__}')
    

    # Methods
    def emoji(self) -> str:
        '''Returns the emoji string representation of the tile.'''
        if self.__tile_type == TileType.WALL:
            return '🧱'
        elif self.__tile_type == TileType.GRASS:
            return '🟩'
        elif self.__tile_type == TileType.EGG:
            return '🥚'
        elif self.__tile_type == TileType.EMPTY_NEST:
            return '🐥'
        elif self.__tile_type == TileType.FULL_NEST:
            return '🐣'
        elif self.__tile_type == TileType.FRYING_PAN:
            return '🍳'
