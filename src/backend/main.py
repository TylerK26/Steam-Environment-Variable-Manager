"""This will be the file that actually houses the main codebase the ui will work with"""

from pathlib import Path
from game_management import get_game_ids, create_game_objects
import json

# Ok so i need to make it so that there's actually memory for this program so it doesn't redo
# API requests every time that it runs, I'll start making config files and stuff

def create_config_file(config_folder: Path, config_file: Path ) -> None:
    """Creates config file for app (If it doesn't already exist), then create
       Default settings based on user input"""
    config_folder.mkdir(parents=True, exist_ok=True)
    with open(config_file, 'w', encoding='utf-8') as file:
        # I will be sleeping now but so i remember tomorrow, this needs to
        # Write a json to the file so it can have the list of game objects in it
        # Without crying
        

def populate_config(config_file: Path, compat_path: Path, local_config_path: Path) -> None:
    """Use functions from game_management to create dictionary for config"""
    ids = get_game_ids(compat_path)
    with open(config_file, 'w', encoding='utf-8') as file:
        game_list = create_game_objects(ids, local_config_path)
        
        
        
    
def main() -> None:
    # These will become a part of config in the future, so the user
    # Doesn't need to always input compatdata path on startup
    # And I'll automatically find user localconfig
    local_config_path = Path('/home/tylerk/.steam/steam/userdata/448133338/config/')
    compat_path = Path('/home/tylerk/.steam/steam/steamapps/compatdata/')

    config_folder = Path('~/.config/proton_var_manager/').expanduser()
    config_file = Path('~/.config/proton_var_manager/config.txt').expanduser()
    create_config_file(config_folder, config_file)
    populate_config(config_file, compat_path, local_config_path)

if __name__ == "__main__":
    main()