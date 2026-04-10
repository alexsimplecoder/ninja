import os
result = open("result.py", "w")
result.write("#main.py\n\n")
f = open("game.py", "r")
result.write(f.read())

result.write("\n\n #editor.py\n\n")
result.write(open("editor.py", "r").read())
for file_name in os.listdir("scripts"):
    if file_name[-3:] == ".py":
        result.write(f"\n\n #{file_name}\n\n")
        result.write(open(f"scripts/{file_name}", "r").read())