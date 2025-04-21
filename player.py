import utils
import yaml
import os
PARSE_MODEL = yaml.safe_load(open("./settings.yaml", "r"))["parse_model"]
print("PARSE_MODEL:",PARSE_MODEL)

parse_query = """
    # Background:
    An agent is playing the game of Adversarial Taboo. In this game, there are two players, an attacker and a defender.
    At the beginning, the attacker is assigned a target word, with which the defender is not informed. The task of the attacker is to induce the defender to utter the target word unconciously, then the attacker win the game. However, the attacker is not allow to utter the target word, otherwise the attacker loses.
    At the same time, the defender tries to figure out the target word. If the defender identifies the target word, he can say "I know the word! It is `target word`!". Then the defender wins. Remember, the defender can only guess the word once, otherwise he will directly lose the game.
    
    
    # Task:
    Your job is to parse the agent's response to the game and respond with what the agent has decided to speak as a player.
    If the agent decides to guess the target word, please format the response as "I know the word! It is `target word`!". 
    Please do not include any other information, just respond with the agent's decision as a player.
    Several examples: 
    
    The agent respond: FINAL ANSWER:
<answer>I'll start by saying: 'I'm going to the stadium to watch a baseball game and run around the grass.'\n Your turn, defender.</answer>
    You should respond with: I'm going to the stadium to watch a baseball game and run around the grass.
    
    The agent respond: I think the word may be 'apple'.
    You should respond: I know the word! It is apple!
    
    The agent respond: I'll play the role of the defender. Based on the attacker's previous statements, I'll try to infer the target word.
    From the attacker's first statement, "I'm thinking of something that is often eaten for breakfast," I can infer that the target word is likely a type of food that is commonly consumed in the morning.
    The attacker's second statement, "Something you might find in a fruit salad," suggests that the target word is a type of fruit.
    With this information, my response is:
    "Is it a type of citrus fruit?"
    You should respond: "Is it a type of citrus fruit?"

    Now, The agent gives the following response to the game:
    {response}
    
    # Your Resonpse:
"""
class Player:
    def __init__(self, model="gpt-4o",exp_path="none"):
        self.model = model
        self.exp_path = exp_path
        self.use_dynamic_cheatsheet = False
        if "none" in exp_path.lower():
            self.experience =  None
        else:
            if exp_path.endswith("dc"):
                self.use_dynamic_cheatsheet = True
            with open(exp_path+".txt",'r') as f:
                self.experience = f.read()
                print(self.experience)
                self.num_exp_round = exp_path.split("_")[-1]
                f.close()
            if self.use_dynamic_cheatsheet:
                with open("./generator.txt",'r') as f:
                    self.generator_prompt = f.read()
                    f.close()
                with open("reflector.txt","r") as f:  
                    self.reflector_prompt = f.read()
                    f.close()
    def __str__(self):
        return f"{self.model} {'w/' if self.experience is not None else 'w/o'} exp{'_'+self.num_exp_round if self.experience is not None else ''}"
    def generate_response(self, query):
        content = query
        if self.use_dynamic_cheatsheet:
            content = self.generator_prompt.replace("[[CHEATSHEET]]",self.experience)
            content = content.replace("[[QUESTION]]",query)
        raw_response = utils.generate_response([{"role": "user", "content": content}], model=self.model)
        print("THOUGHT:", raw_response)
        response = self._parse_response(raw_response)
        return response
    def _parse_response(self, response):
        return utils.generate_response(
            [{"role": "user", "content": parse_query.format(response=response)}],
            model=PARSE_MODEL
        )
        
    def reflect(self, history, feedback):
        content = self.reflector_prompt.replace("[[PREVIOUS_CHEATSHEET]]",self.experience)\
            .replace("[[GAME_CONTENT]]",history)\
                .replace("[[FEEDBACK]]",feedback)
        new_cheetsheet = utils.generate_response([{'role':"user","content":content}],model=self.model)
        return new_cheetsheet
