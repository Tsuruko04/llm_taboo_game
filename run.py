import game

if __name__ == "__main__":
   game = game.TabooGame(target_word="apple", max_turns=5)
   game.run()