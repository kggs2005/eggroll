import sys
from classes.GameController import GameController


def main():
    # Terminal input: python EggRoll.py levelfilename.in

    # Must have at least 2 arguments
    if len(sys.argv) < 2:
        print('The game requires a filename to start.', file=sys.stderr)
        return
    
    # Obtain filename
    filename = ' '.join(sys.argv[1:])

    try:
        # Attempt to search for the file given the filename
        file = open(f'levels/{filename}', 'r', encoding='utf8')

    except FileNotFoundError:
        # Filename does not exist
        print(f'Level filename \'{filename}\' does not exist.')

    else:
        # Create a game controller and load the file
        game_controller = GameController(file)
        game_controller.display_ui()


main()
