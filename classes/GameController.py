from os import name, path, system

from .Game import Game
from .GameState import GameState
from .Move import Move, MoveType
from .Tile import Tile

class GameController:
    '''
    Controller for games of EggRoll.
    Handles the terminal UI for the program.
    '''


    # Constructor
    def __init__(self, file):
        '''Creates a new game with a level file'''
        # Get necessary data
        lines = file.readlines()
        moves = int(lines[1].strip())
        grid = [[Tile(emoji) for emoji in row.strip()] for row in lines[2:] if row]

        # Close file as it is no longer needed
        file.close()

        # Create new game
        self.__game = Game(GameState(grid, (), moves, 0))
    

    # Methods
    def __clear(self) -> None:
        '''Clears the screen. Adapts to system OS.'''
        system('cls' if name == 'nt' else 'clear')
    

    def __char_to_move(self, char: str) -> Move:
        '''Converts the characters u, d, l, r to their respective Moves.'''
        if char == 'u':
            return Move(MoveType.UP)
        elif char == 'd':
            return Move(MoveType.DOWN)
        elif char == 'l':
            return Move(MoveType.LEFT)
        elif char == 'r':
            return Move(MoveType.RIGHT)


    def display_ui(self) -> None:
        '''Update the UI for every state change.'''
        while not self.__game.is_over():
            # Show current game state
            self.__clear()
            print(self.__game.current_game_state().state_str())

            # Wait for input
            entered_moves = input('Enter move/s: ')

            # Perform each valid move but immediately stop if the game is over 
            valid_moves = (char for char in entered_moves.replace(' ', '').lower() if char in ('u', 'd', 'l', 'r'))
            for char in valid_moves:
                if self.__game.is_over():
                    break
                move = self.__char_to_move(char)
                self.__game.make_move(move)
        
        # Show final game state
        self.__clear()
        print(self.__game.current_game_state().state_str())
        print(f'\nGame Over! Score: {self.__game.current_game_state().get_points()}\n')
