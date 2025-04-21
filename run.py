import yaml
import game
import argparse
import random
import time
random.seed(time.time_ns())
parser = argparse.ArgumentParser()
parser.add_argument("--num_exp","-n",type=int,default=10)
parser.add_argument("--max_turns","-t",type=int,default=5)
parser.add_argument("--words_path","-w",type=str,default="./data/all_target_words.txt")
parser.add_argument("--settings", "-s", type=str, default="./settings/settings.yaml")
if __name__ == "__main__":
   all_words = []
   args = parser.parse_args()
   n = args.num_exp
   max_turns = args.max_turns
   with open(args.words_path,"r") as f:
      for line in f.readlines():
         all_words.append(line.strip().strip('\n'))
   sampled_words = random.sample(all_words,k=n)
   settings = yaml.safe_load(open(args.settings))
   for i,w in enumerate(sampled_words):
      print(f"Running on sample {i+1}/{len(sampled_words)}")
      tbgame = game.TabooGame(target_word= w,settings=settings ,max_turns=max_turns)
      tbgame.run()
      tbgame.log()