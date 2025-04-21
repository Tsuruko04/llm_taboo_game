import os
result = {}
for log in os.listdir("./log"):
    with open(f"./log/{log}","r") as f:
        ATK = None
        DEF = None
        GAMERESULT = None
        for line in f.readlines():
            if line.startswith("Attacker"):
                ATK = line.split(':')[-1].strip()
            if line.startswith("Defender"):
                DEF = line.split(':')[-1].strip()
            if line.startswith("GameResult"):
                GAMERESULT = line.split(".")[-1]
        if ATK and DEF and GAMERESULT:
            if f"{ATK} vs {DEF}" not in result:
                result[f"{ATK} vs {DEF}"] = [0,0,0]
            if "ATTACKER" in GAMERESULT:
                result[f"{ATK} vs {DEF}"][0]+=1
            elif "DEFENDER" in GAMERESULT:
                result[f"{ATK} vs {DEF}"][1] += 1
            else:
                result[f"{ATK} vs {DEF}"][2] += 1
                
print("| Attacker vs Defender | Attacker Wins | Denfender Wins | Tied |")
for k,v in result.items():
    print(f"| {k} | {v[0]} | {v[1]} | {v[2]} |")