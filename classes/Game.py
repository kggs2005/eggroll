import copy
from .GameState import GameState
from .Move import Move, MoveType
from .Tile import Tile, TileType


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
        The new game state has the same grid and number of points,
        but a new move has been added to the previous moves,
        and the number of remaining moves is decreased by 1.
        '''
        # Set up variables for new game state
        grid = self.current_game_state().get_grid()
        new_previous_moves = (*self.current_game_state().get_previous_moves(), move)
        new_remaining_moves = self.current_game_state().get_remaining_moves() - 1
        points = self.current_game_state().get_points()

        # Create new game state and add it in the game state history
        self.add_game_state(GameState(grid, new_previous_moves, new_remaining_moves, points))


    def next_game_state(self) -> GameState | None:
        '''
        Returns the next game state based on the current game state and the previous move.
        Returns None if the current game state is final or if the game just started.
        '''
        # Return None if the current game state is final or if the game just started.
        if self.current_game_state().is_final() or len(self.current_game_state().get_previous_moves()) == 0:
            return None

        # Return a copy of the current game state if the eggs can't roll.
        if not self.current_game_state().eggs_are_rolling():
            return copy.deepcopy(self.current_game_state())
        
        # Set up variables for new game state
        new_grid = self.current_game_state().get_grid()
        previous_moves = self.current_game_state().get_previous_moves()
        remaining_moves = self.current_game_state().get_remaining_moves()
        new_points = self.current_game_state().get_points()

        # Make reference to previous move and the number of rows and columns
        move = previous_moves[-1]
        rows = len(new_grid)
        cols = len(new_grid[0])


        # Move Up: iterates from top row to bottom row, from left tile to right tile.
        if move.get_type() == MoveType.UP:
            for i in range(1, rows - 1):
                for j in range(1, cols - 1):
                    this_tile = new_grid[i][j]
                    tile_below = new_grid[i + 1][j]
                    new_points= self.__evaluate_tile(this_tile, tile_below, remaining_moves, new_points)

        # Move Down: iterates from bottom row to top row, from left tile to right tile.
        if move.get_type() == MoveType.DOWN:
            for i in range(1, rows - 1)[::-1]:
                for j in range(1, cols - 1):
                    this_tile = new_grid[i][j]
                    tile_above = new_grid[i - 1][j]
                    new_points = self.__evaluate_tile(this_tile, tile_above, remaining_moves, new_points)

        # Move Left: iterates from left column to right column, from top tile to bottom tile.
        if move.get_type() == MoveType.LEFT:
            for j in range(1, cols - 1):
                for i in range(1, rows - 1):
                    this_tile = new_grid[i][j]
                    tile_right = new_grid[i][j + 1]
                    new_points = self.__evaluate_tile(this_tile, tile_right, remaining_moves, new_points)
        
        # Move Right: iterates from right column to left column, from top tile to bottom tile.
        if move.get_type() == MoveType.RIGHT:
            for j in range(1, cols - 1)[::-1]:
                for i in range(1, rows - 1):
                    this_tile = new_grid[i][j]
                    tile_left = new_grid[i][j - 1]
                    new_points = self.__evaluate_tile(this_tile, tile_left, remaining_moves, new_points)
                
        # Note that iteration is from 1 to rows/cols - 1 because the outer layer of the grid will always be walls.
        
        # Create and return a new game state
        return GameState(new_grid, previous_moves, remaining_moves, new_points)


    def __evaluate_tile(self, this_tile: Tile, ref_tile: Tile, remaining_moves: int, points: int) -> int:
        '''
        Handles the points and the tile changes depending on the current tile and the reference tile.
        Returns the new number of points after the evaluation.
        '''
        # Only evaluate if the reference tile is an egg
        if ref_tile.get_tile_type() != TileType.EGG:
            return points
        
        # If tile is grass and there is an egg below, this tile is now an egg, and the tile below is now grass.
        if this_tile.get_tile_type() == TileType.GRASS:
            this_tile.set_tile_type(TileType.EGG)
            ref_tile.set_tile_type(TileType.GRASS)
        
        # If tile is empty nest and there is an egg below, this tile is now a full nest, and the tile below is now grass.
        # Also, gain 10 points + number of remaining moves (this move is counted).
        elif this_tile.get_tile_type() == TileType.EMPTY_NEST:
            this_tile.set_tile_type(TileType.FULL_NEST)
            ref_tile.set_tile_type(TileType.GRASS)
            points += 10 + remaining_moves

        # If tile is frying pan and there is an egg below, the tile below is now grass.
        # Also, lose 5 points.
        elif this_tile.get_tile_type() == TileType.FRYING_PAN:
            ref_tile.set_tile_type(TileType.GRASS)
            points -= 5
        
        return points
