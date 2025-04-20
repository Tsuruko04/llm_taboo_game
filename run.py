import game
import argparse
import random
parser = argparse.ArgumentParser()
parser.add_argument("--num_exp","-n",type=int,default=10)
parser.add_argument("--max_turns","-t",type=int,default=5)
if __name__ == "__main__":
   all_words = []
   parser.parse_args()
   n = parser.num_exp
   max_turns = parser.max_turns
   with open("./all_target_words.txt","r") as f:
      for line in f.readlines():
         all_words.append(line.strip(" ", '/n'))
   sampled_words = random.choices(all_words,k=n)
   for i,w in enumerate(sampled_words):
      print(f"Running on sample {i+1}/{len(sampled_words)}")
      game = game.TabooGame(target_word= w,max_turns=max_turns)
      game.run()
      game.log()