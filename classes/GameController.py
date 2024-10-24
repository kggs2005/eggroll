from os import name, path, system
from queue import Queue
from sys import argv, stderr
from time import sleep

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
    def __init__(self):
        '''Creates a new game with the terminal arguments'''
        # Requires at least 2 arguments
        if len(argv) < 2:
            print('The game requires a filename to start.', file=stderr)
            return
        
        # Obtain filename from terminal arguments
        filename = ' '.join(argv[1:])

        # Get relative path of level file
        this_path = path.abspath(path.dirname(__file__))
        file_path = path.join(this_path, f'../levels/{filename}')

        try:
            # Attempt to search for the file given the file path
            file = open(file_path, 'r', encoding='utf8')
        except FileNotFoundError:
            # Filename does not exist
            print(f'Level filename \'{filename}\' does not exist.')
        else:
            # Get necessary data
            lines = file.readlines()
            moves = int(lines[1].strip())
            grid = [[Tile(emoji) for emoji in row.strip()] for row in lines[2:] if row]

            # Close file as it is no longer needed
            file.close()

            # Create new game
            self.__game = Game(GameState(grid, (), moves, 0))

            # Display UI
            self.__display_ui()
    

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


    def __display_ui(self) -> None:
        '''Update the UI for every state change.'''
        # In case of multiple moves for one input, queue the moves.
        max_moves = self.__game.current_game_state().get_remaining_moves()
        move_queue: Queue[Move] = Queue(max_moves)

        while not self.__game.is_over():
            # Show current game state
            self.__clear()
            print(self.__game.current_game_state().state_str())

            # If eggs are rolling, animate it
            if self.__game.current_game_state().eggs_are_rolling():
                sleep(0.1)
                self.__game.add_game_state(self.__game.next_game_state())
                
            # Otherwise, if there are any queued moves, perform the move
            elif not move_queue.empty():
                self.__game.make_move(move_queue.get_nowait())
            
            # Otherwise ask for the player's input
            else:
                # Wait for input
                entered_moves = input('Enter move/s: ')

                # Perform each valid move but immediately stop if the game is over 
                valid_moves = (char.lower() for char in entered_moves if char.lower() in 'udlr')
                for char in valid_moves:
                    if move_queue.full():
                        break
                    move = self.__char_to_move(char)
                    move_queue.put_nowait(move)
        
        # Show final game state
        self.__clear()
        print(self.__game.current_game_state().state_str())
        print(f'\nGame Over! Score: {self.__game.current_game_state().get_points()}\n')
