
word1 = "Hello"
word2 = "World"
openscad_path = "C:/Program%20Files/OpenSCAD/openscad.com"
program_path = "C:/Users/David/Documents/Projects/cadwebsite/names.scad"
var1 = f'-D name1=\"{word1}\"'
var2 = f'-D name2=\"{word2}\"'
build = f" -o './test.stl' '{program_path}'"
command = f"{openscad_path} {var1} {var2} {build}"
print(command)

# execute command
import os
os.system(command)