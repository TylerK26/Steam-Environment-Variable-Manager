"""This file is for:
   Finding games installed with proton
   Fetching their current environment variables
   Saving their environment variables"""

from pathlib import Path
import requests
import vdf

# Each game will get it's own object
class Game:
    """Creates game for future UI which includes it's name, 
            steam id, and current environment variables"""
    def __init__(self, title: str, proton_id: int, variable_list: list[str]) -> None:
        self.title = title
        self.id = proton_id
        self.vars = variable_list
    def __str__(self) -> str:
        return self.title
    def get_id(self) -> int:
        """Return proton id"""
        return self.id

def get_game_name(game_id: int) -> str:
    """Get game name from game id"""
    game_url = f"https://store.steampowered.com/api/appdetails?appids={game_id}"
    try:
        response = requests.get(game_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        game_name = str(data[str(game_id)]['data']['name'])
        return game_name
    except requests.exceptions.RequestException as e:
        print(f"An error occured for this game: {e}")
    except KeyError:
        pass

def get_game_ids(path: Path) -> list[int]:
    """Make list of all game ids to later create objects of"""
    game_ids = []
    # Check all compatdata folders
    for folder in path.iterdir():
        if int(folder.name) != 0:
            game_ids.append(int(folder.name))
    return game_ids

def get_game_env_vars(game_ids: list[int], directory: Path) -> dict[str, list[str]]:
    """Get all environment variables for each game, it's a list of lists which I find scary
       I'm so happy there's a vdf parser package that I can use because I did NOT want 
       to have to do that myself"""
    # I'm going to hard code this directory for now, but later I definitely need to not do that so
    # Other people can actually use the software
    dict_of_vars = {}
    for i in game_ids:
        temp_list: list[str] = []
        local_config = directory / 'localconfig.vdf'
        with open(local_config, 'r+', encoding="utf-8") as file:
            f = vdf.load(file)
            app_info = f['UserLocalConfigStore']['Software']['Valve']['Steam']['apps'][str(i)]
            try:
                # Get environment variables as string, separate them as individual parts of a list,
                # Then make key-value pair in dictionary for each game
                env_vars_str = app_info['LaunchOptions']
                env_vars_list = env_vars_str.strip().split()
                for word in env_vars_list:
                    if word == "%command%":
                        break
                    temp_list.append(word)
                dict_of_vars[get_game_name(i)] = temp_list
            except KeyError:
                print("This game does not have launch options yet, making keys now")
                # Go to key in vdf, make launchoptions with empty string as value,
                # save to currently open vdf
                # I honestly can't believe I did this first try without breaking anything
                f['UserLocalConfigStore']['Software']['Valve']['Steam']['apps'][str(i)]['LaunchOptions'] = ''
                dict_of_vars[get_game_name(i)] = []
                vdf.dump(f, file, pretty=True)
    return dict_of_vars

def create_game_objects(game_ids: list[int], directory: Path, local_json: dict, use_local: bool = False) -> list[Game]:
    """Create all instances of Game needed for each game in game_ids"""
    temp_games: list[Game] = []
    if use_local:
        local_games = local_json['games']
        count = 1
        for key in local_games:
            if key == 'null':
                continue
            temp_games.append(Game(key, game_ids[count], local_games[key]))
            count += 1
        return temp_games
    game_environment_vars = get_game_env_vars(game_ids, directory)
    for i in game_ids:
        title = get_game_name(i)
        for key in game_environment_vars.items():
            if key[0] == title:
                temp_game = Game(title, i, game_environment_vars[key[0]])
                temp_games.append(temp_game)
    return temp_games

def main() -> None:
    """Since this only runs when calling the file directly, I can just use this
    area for testing new features I might be implementing"""
    #ids = get_game_ids(Path('/home/tylerk/.steam/steam/steamapps/compatdata/'))
    #temp = create_game_objects(ids, '/home/tylerk/.steam/steam/userdata/448133338/config/')
    #for i in temp:
    #    print(f"Game: {i.title}, ID: {i.id}, Vars: {i.vars}")


if __name__ == "__main__":
    main()
