import yaml
import utils
import enum
import time
from player import Player
class GameResult(enum.Enum):
    NONE = 0
    ATTACKER_WINS = 1
    DEFENDER_WINS = 2
    TIED = 3
class TabooGame:
    def __init__(self, target_word, max_turns=5):
        self.target_word = target_word
        self.max_turns = max_turns
        self.turns = 0
        self.history = []
        self.game_result = GameResult.NONE
        settings = yaml.safe_load(open("./settings.yaml"))
        agents = settings["agents"]
        self.players = {
            "attacker": Player(model=agents["attacker"]),
            "defender": Player(model=agents["defender"])
        }
        print(
            f"""
                Attacker: {self.players["attacker"]}\n
                Defender: {self.players["defender"]}\n
                Target Word: {self.target_word}\n
                Max Turns: {self.max_turns}\n
                ---\n
                """
        )
    
    def run(self):
        while self.turns < self.max_turns:
            print(f"----------TURN {self.turns + 1}/{self.max_turns}----------")
            query = utils.convert_game_history_to_query(self.history, self.target_word, self.max_turns)
            response = self.players["attacker"].generate_response(query)
            print(f"ATTACKER SPOKE: {response}")
            self.history.append({"role":"attacker", "content":response})
            query = utils.convert_game_history_to_query(self.history, self.target_word, self.max_turns)
            response = self.players["defender"].generate_response(query)
            print(f"DEFENDER SPOKE: {response}")
            self.history.append({"role":"defender", "content":response})
            if "i know the word" in response.lower():
                if self.target_word in response.lower():
                    print("DEFENDER WINS")
                    self.game_result = GameResult.DEFENDER_WINS
                    return GameResult.DEFENDER_WINS
                else:
                    print("ATTACKER WINS")
                    self.game_result = GameResult.ATTACKER_WINS
                    return GameResult.ATTACKER_WINS
            else:
                if self.target_word in response.lower():
                    print("ATTACKER WINS")
                    self.game_result = GameResult.ATTACKER_WINS
                    return GameResult.ATTACKER_WINS

            self.turns += 1
        print("TIED")
        self.game_result = GameResult.TIED
        return GameResult.TIED
            
    def log(self):
        with open(f"./log/game_history_{time.time()}.txt","w+") as f:
            f.write(
                f"""
                Attacker: {self.players["attacker"]}\n
                Defender: {self.players["defender"]}\n
                Target Word: {self.target_word}\n
                Max Turns: {self.max_turns}\n
                ---\n
                """
            )
            history_str = ""
            for i, message in enumerate(self.history):
                history_str += "\n  - {}: {}".format(message['role'], message['content'])
            f.write(history_str)
            f.write(str(self.game_result))
            