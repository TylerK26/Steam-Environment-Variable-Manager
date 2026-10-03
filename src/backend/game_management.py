"""This file is for:
   Finding games installed with proton
   Fetching their current environment variables
   Saving their environment variables"""

import requests
import os
import vdf

# Each game will get it's own object
class Game:
    def __init__(self, title: str, proton_id: int, variable_list: list[str]) -> None:
        """Creates game for future UI which includes it's name, 
        steam id, and current environment variables"""
        self.title = title
        self.id = proton_id
        self.vars = variable_list

game_ids = list[int]
games = list[Game]

def get_game_name(game_id: int) -> str:
    """Get game name from game id"""
    game_url = f"https://store.steampowered.com/api/appdetails?appids={game_id}"

    try:
        response = requests.get(game_url)
        response.raise_for_status()
        data = response.json()
        game_name = str(data[str(game_id)]['data']['name'])
        return game_name
    except requests.exceptions.RequestException as e:
        print(f"An error occured for this game: {e}")
    except KeyError:
        return None

def get_game_ids(path: str) -> list[int]:
    """Make list of all game ids to later create objects of"""
    game_ids_fun = []
    # Check all compatdata folders
    with os.scandir(path) as game_folder:
        for folder in game_folder:
            if folder.is_dir() and int(folder.name) != 0:
                game_ids_fun.append(int(folder.name))
    return game_ids_fun

def get_game_env_vars(game_ids: list[int]) -> list[list[str]]:
    """Get all environment variables for each game, it's a list of lists which I find scary
       I'm so happy there's a vdf parser package that I can use because I did NOT want 
       to have to do that myself"""
    # I'm going to hard code this directory for now, but later I definitely need to not do that so
    # Other people can actually use the software
    main_list = list[list[str]]
    for i in game_ids:
        temp_list = list[str]
        with open("/home/tylerk/.local/share/Steam/userdata/448133338/config/localconfig.vdf", 'r') as file:
            f = vdf.load(file)
            print(f['UserLocalConfigStore']['Software']['Valve']['Steam']['apps'][str(i)])

# This can be done later when I can actually get environment variables
#def create_game_objects(game_ids: list[int]) -> list[Game]:
#    """Create all instances of Game needed for each game in game_ids"""
#    temp_games = list[Game]
#    for i in game_ids:
#        temp_title = get_game_name(i)
#        # To be continuted when I can actually get game variables
#        temp_game = Game(temp_title, i, )

def main() -> None:
    id_list = get_game_ids("/home/tylerk/.steam/steam/steamapps/compatdata/")
    get_game_env_vars(id_list)

if __name__ == "__main__":
    main()