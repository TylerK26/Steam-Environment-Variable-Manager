"""This file is for:
   Finding games installed with proton
   Fetching their current environment variables
   Saving their environment variables"""

import requests
import os

# Each game will get it's own object
class Game:
    def __init__(self, title: str, proton_id: int, variable_list: list[str]) -> None:
        """Creates game for future UI which includes it's name, 
        steam id, and current environment variables"""
        self.title = title
        self.id = proton_id
        self.vars = variable_list

game_ids = list[int]

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
    with os.scandir(path) as game_folder:
        for folder in game_folder:
            if folder.is_dir() and int(folder.name) != 0:
                game_ids_fun.append(int(folder.name))
    return game_ids_fun

def main() -> None:
    for id in get_game_ids('/home/tylerk/.steam/steam/steamapps/compatdata/'):
        print(get_game_name(id))
if __name__ == "__main__":
    main()