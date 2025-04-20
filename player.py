import utils
import yaml
PARSE_MODEL = yaml.safe_load(open("./settings.yaml", "r"))["parse_model"]
print("PARSE_MODEL:",PARSE_MODEL)

parse_query = """
    # Background
    Play the game of Adversarial Taboo. In this game, there are two players, an attacker and a defender.
    At the beginning, the attacker is assigned a target word, with which the defender is not informed. The task of the attacker is to induce the defender to utter the target word unconciously, then the attacker win the game. However, the attacker is not allow to utter the target word, otherwise the attacker loses.
    At the same time, the defender tries to figure out the target word. If the defender identifies the target word, he can say "I know the word! It is `target word`!". Then the defender wins. Remember, the defender can only guess the word once, otherwise he will directly lose the game.
    
    The agent gives the following response to the game:
    {response}
    
    # Task
    Your job is to parse the agent's response to the game and respond with what the agent has decided to speak as a player.
    If the agent decides to guess the target word, please format the response as "I know the word! It is `target word`!". 
    Please do not include any other information, just respond with the agent's decision as a player.
"""
class Player:
    def __init__(self, model="gpt-4o"):
        self.model = model
        self.experience =  None
        
    def generate_response(self, query):
        raw_response = utils.generate_response([{"role": "user", "content": query}], model=self.model)
        print("THOUGHT:", raw_response)
        response = self._parse_response(raw_response)
        return response
    def _parse_response(self, response):
        return utils.generate_response(
            [{"role": "user", "content": parse_query.format(response=response)}],
            model=PARSE_MODEL
        )