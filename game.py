import yaml
import utils
from player import Player
class TabooGame:
    def __init__(self, target_word, max_turns=5):
        self.target_word = target_word
        self.max_turns = max_turns
        self.turns = 0
        self.history = []
        
        settings = yaml.safe_load(open("./settings.yaml"))
        agents = settings["agents"]
        self.players = {
            "attacker": Player(model=agents["attacker"]),
            "defender": Player(model=agents["defender"])
        }
    
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
                    return
                else:
                    print("ATTACKER WINS")
                    return
            else:
                if self.target_word in response.lower():
                    print("ATTACKER WINS")
                    return

            self.turns += 1
        print("TIED")
            
