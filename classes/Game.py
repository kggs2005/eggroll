from .GameState import GameState
from .Move import Move, MoveType
from .Tile import TileType


class Game():
    '''
    Represents a game of EggRoll.
    A game is described by a starting level and a history of GameStates that track the state of the game.
    '''


    # Constructor
    def __init__(self, first_state: GameState):
        '''Initiates a game with the first game state.'''
        self.__game_states = [first_state]


    # Getters
    def game_states(self) -> list[GameState]:
        '''Returns a copy of the list of the game's game states.'''
        return list(self.__game_states)


    def current_game_state(self) -> GameState:
        '''Returns a copy of the current (latest) game state'''
        return self.__game_states[-1]


    # Methods
    def add_game_state(self, new_game_state: GameState) -> None:
        '''Adds a new game state to the game's history of game states'''
        self.__game_states.append(new_game_state)
    

    def is_over(self) -> bool:
        '''Whether the game is over (no more moves or no more live eggs)'''
        return self.current_game_state().is_final()
    

    def make_move(self, move: Move) -> None:
        '''
        Makes a move to progress the game.
        Creates a new game state based on the move and stores it in its history of game states.
        '''
        # Set up variables for new game state
        new_grid = self.current_game_state().get_grid()
        new_previous_move = (*self.current_game_state().get_previous_moves(), move)
        new_remaining_moves = self.current_game_state().get_remaining_moves() - 1
        new_points = self.current_game_state().get_points()

        # Set number of rows and columns as new variables
        rows = len(new_grid)
        cols = len(new_grid[0])

        # Move up: iterates from top row to bottom row, from left tile to right tile
        if move.get_type() == MoveType.UP:
            for i in range(rows):
                for j in range(cols):
                    # If tile is grass and there is an egg below, this tile is now an egg, and the tile below is now grass.
                    if new_grid[i][j].get_tile_type() == TileType.GRASS:
                        if new_grid[i + 1][j].get_tile_type() == TileType.EGG:
                            new_grid[i][j].set_tile_type(TileType.EGG)
                            new_grid[i + 1][j].set_tile_type(TileType.GRASS)

                    # If tile is empty nest and there is an egg below, this tile is now a full nest, and the tile below is now grass.
                    # Also, gain 10 points + number of remaining moves (this move is counted).
                    elif new_grid[i][j].get_tile_type() == TileType.EMPTY_NEST:
                        if new_grid[i + 1][j].get_tile_type() == TileType.EGG:
                            new_grid[i][j].set_tile_type(TileType.FULL_NEST)
                            new_grid[i + 1][j].set_tile_type(TileType.GRASS)
                            new_points += 10 + self.current_game_state().get_remaining_moves()

                    # If tile is frying pan and there is an egg below, the tile below is now grass.
                    # Also, lose 5 points.
                    elif new_grid[i][j].get_tile_type() == TileType.FRYING_PAN:
                        if new_grid[i + 1][j].get_tile_type() == TileType.EGG:
                            new_grid[i + 1][j].set_tile_type(TileType.GRASS)
                            new_points -= 5

        # Notes to CJ:
        # - I'll leave these 3 other moves to you.
        # - The code so far only moves the eggs one tile in the given direction. The actual game must move the eggs all the way in that direction.
        # - The game must also animate each movement. CS11_241_MP1.pdf "6.2 Causing a Time Delay" should tell you how to make a terminal delay.
        
        # Move down: iterates from bottom row to top row, from left tile to right tile
        elif move.get_type() == MoveType.DOWN:
            pass

        # Move left: iterates from left column to right column, from top tile to bottom tile
        elif move.get_type() == MoveType.LEFT:
            pass

        # Move right: iterates from right column to left column, from top tile to bottom tile
        elif move.get_type() == MoveType.RIGHT:
            pass

        

        # Create new game state and add it in the game state history
        self.add_game_state(GameState(new_grid, new_previous_move, new_remaining_moves, new_points))
