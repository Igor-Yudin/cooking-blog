import sass
import sys
import os

# if sys.argv[0] == "":
#     return 0
# if sys.argv[1] == "":
#     return
os.chdir(os.path.dirname(os.path.abspath(__file__)))
with open(sys.argv[1], 'r') as file_obj:
    text = file_obj.read()
code = sass.compile(string = text)

filename, extension = os.path.splitext(sys.argv[1])
filename = filename.split('\\')[-1]

with open("..\css\{0}.css".format(filename), "w") as file_obj:
    file_obj.write(code)