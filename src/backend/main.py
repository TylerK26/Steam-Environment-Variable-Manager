"""This will be the file that actually houses the main codebase the ui will work with"""

import json
from pathlib import Path
from game_management import get_game_ids, create_game_objects, get_game_env_vars

# Ok so i need to make it so that there's actually memory for this program so it doesn't redo
# API requests every time that it runs, I'll start making config files and stuff

def create_config_file(config_folder: Path, config_file: Path,
                        compat_path: str, local_config_path: str) -> None:
    """Creates config file for app, then create
       Default settings based on user input"""
    # Fill in json info with
    temp_json: dict[str, dict[str, str]] = {}
    temp_json['config'] = {}
    temp_json['config']['compat_path'] = compat_path
    temp_json['config']['local_config_path'] = local_config_path

    config_folder.mkdir(parents=True, exist_ok=True)
    with open(config_file, 'w', encoding='utf-8') as file:
        json.dump(temp_json, file, indent=4)
        

def populate_config(config_file: Path) -> None:
    """Use functions from game_management to create dictionary for config"""
    with open(config_file, 'r', encoding='utf-8') as file:
        f = json.load(file)
    game_ids = get_game_ids(Path(f['config']['compat_path']))
    game_dictionary = get_game_env_vars(game_ids, Path(f['config']['local_config_path']))
    f['games'] = game_dictionary
    with open(config_file, 'w', encoding='utf-8') as file:
        json.dump(f, file, indent=4)
        
    
def main() -> None:
    # These should stay hardcoded cause the user doesn't get to decide
    # Where configs are saved, I do
    config_folder = Path('~/.config/proton_var_manager/').expanduser()
    config_file = Path('~/.config/proton_var_manager/config.json').expanduser()

    if not config_file.is_file():
        local_config_str: str = input('Please provide directory for ' \
        'localconfig.vdf, usually in /home/{user}/.steam/steam/userdata/{account id}/config/: ')

        compat_str = input('Please provide directory for ' \
        'compatdata, usually in /home/{user}/.steam/steam/steamapps/compatdata/: ')

        create_config_file(config_folder, config_file, compat_str, local_config_str)
        populate_config(config_file)
    with open(config_file, 'r', encoding='utf-8') as file:
        f = json.load(file)
    local_config = Path(f['config']['local_config_path'])
    compat_path = Path(f['config']['compat_path'])
    game_ids = get_game_ids(compat_path)
    games = create_game_objects(game_ids, local_config, f, use_local=True)


if __name__ == "__main__":
    main()