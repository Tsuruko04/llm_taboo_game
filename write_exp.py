import os
import utils
NUM_EXP = 5
ROLE = "defender"
model = "llama3.1-8b"
sys_prompt = """
You are an experienced party game player.
# Background:
The game of Adversarial Taboo. In this game, there are two players, an attacker and a defender.
At the beginning, the attacker is assigned a target word, with which the defender is not informed. The task of the attacker is to induce the defender to utter the target word unconciously, then the attacker win the game. However, the attacker is not allow to utter the target word, otherwise the attacker loses.
At the same time, the defender tries to figure out the target word. If the defender identifies the target word, he can say "I know the word! It is `target word`!". Then the defender wins. Remember, the defender can only guess the word once, otherwise he will directly lose the game.

# Game Logs:
{gamelogs}

# Task:
Given several game logs, you need to read them carefully and conclude strategies to win the game as the {role}.

# Response:
"""

gamelogs = ""
for log in os.listdir("./log")[:5]:
    with open(f"./log/{log}","r") as f:
        gamelogs+=(f.read()+"\n")
with open(f"./exp/{model}_{NUM_EXP}","w+") as f:
    exp = utils.generate_response([{'role':"system","content":sys_prompt.format(role=ROLE,gamelogs=gamelogs)}],model=model)
    print(exp)
    f.write(exp)