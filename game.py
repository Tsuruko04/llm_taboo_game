import os
import utils
import enum
import time
import re
from player import Player
class GameResult(enum.Enum):
    NONE = 0
    ATTACKER_WINS = 1
    DEFENDER_WINS = 2
    TIED = 3
class TabooGame:
    def __init__(self, target_word, settings,max_turns=5):
        self.target_word = target_word
        self.max_turns = max_turns
        self.turns = 0
        self.history = []
        self.game_result = GameResult.NONE
        agents = settings["agents"]
        self.exp_path = settings["experience_path"]
        self.players = {
            "attacker": Player(model=agents["attacker"],exp_path=self.exp_path["attacker"],parse_model=settings["parse_model"]),
            "defender": Player(model=agents["defender"],exp_path=self.exp_path["defender"],parse_model=settings["parse_model"])
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
        attacker = self.players["attacker"]
        defender = self.players["defender"]
        while self.turns < self.max_turns:
            print(f"----------TURN {self.turns + 1}/{self.max_turns}----------")

            query = utils.convert_game_history_to_query(self.history, self.target_word, self.max_turns)
            response = attacker.generate_response(query)
            print(f"ATTACKER SPOKE: {response}")
            self.history.append({"role":"attacker", "content":response})
            response = re.sub(r'[^a-zA-Z]', ' ', response)
            if self.target_word in response.lower().split():
                print("DEFENDER WINS")
                self.game_result = GameResult.DEFENDER_WINS
                return GameResult.DEFENDER_WINS
            query = utils.convert_game_history_to_query(self.history, self.target_word, self.max_turns)
            response = defender.generate_response(query)
            print(f"DEFENDER SPOKE: {response}")
            self.history.append({"role":"defender", "content":response})
            response = re.sub(r'[^a-zA-Z]', ' ', response)
            if "i know the word" in response.lower():
                if self.target_word in response.lower().split():
                    print("DEFENDER WINS")
                    self.game_result = GameResult.DEFENDER_WINS
                    return GameResult.DEFENDER_WINS
                else:
                    print("ATTACKER WINS")
                    self.game_result = GameResult.ATTACKER_WINS
                    return GameResult.ATTACKER_WINS
            else:
                if self.target_word in response.lower().split():
                    print("ATTACKER WINS")
                    self.game_result = GameResult.ATTACKER_WINS
                    return GameResult.ATTACKER_WINS

            self.turns += 1
        print("TIED")
        self.game_result = GameResult.TIED
        return GameResult.TIED
            
    def log(self, dir="log"):
        if not os.path.exists(dir):
            os.mkdir(dir)
        history_str = ""
        for i, message in enumerate(self.history):
            history_str += "\n  - {}: {}".format(message['role'], message['content'])
        with open(f"{dir}/game_history_{time.time()}.txt","w+") as f:
            f.write(
                f"Attacker: {self.players['attacker']}\nDefender: {self.players['defender']}\nTarget Word: {self.target_word}\nMax Turns: {self.max_turns}\n---"
            )
            f.write(history_str+"\n")
            f.write(str(self.game_result))
            f.close()
        for role, player in self.players.items():
            if player.use_dynamic_cheatsheet:
                if self.game_result == GameResult.ATTACKER_WINS:
                    result = "Attacker has won this game."
                elif self.game_result == GameResult.DEFENDER_WINS:
                    result = "Defender has won this game."
                else:
                    result = "Game is tied"
                with open(self.exp_path[role]+".txt","w+",encoding="utf-8") as f:
                    exp = player.reflect(history=utils.GAME_RULE_PROMPTS[0].format(max_turns=self.max_turns)+history_str,feedback=f"Target Word is {self.target_word}. {result}")
                    # import pdb
                    # pdb.set_trace()
                    f.write(exp)       
            elif player.experience is not None:
                exp = "Here are several game experiences:"
                for log in os.listdir(dir)[-int(player.num_exp_round):]:
                    with open(dir+"/"+log, "r") as f:
                        exp+=("\n"+f.read())
                with open(self.exp_path[role]+".txt","w+",encoding="utf-8") as f:
                    f.write(exp)
                     
                
        
       
                