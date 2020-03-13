import re

path = "/<username>/<password>/<fsd>"

pattern = "<(.+?)>"

pat = re.compile(pattern)


matched_ans = pat.findall(path)
print(type(matched_ans))
print(matched_ans)

for i in matched_ans:
    print (i)


pattern = "<(.+?)>"

pattern = "(.*?)[<.*>].*"

pat = re.compile(pattern)

matched_ans = pat.findall(path)

print (matched_ans)


def add ():
    return 1 + 2

m = {}

print (add(**m))