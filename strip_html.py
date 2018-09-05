import re
import json

allTweetsRegex = '</a></li><li>(.*?)<a'
fbMessageRegex = '<span class="user">Derek Dunlea</span>(.*?)<p>(.*?)</p><div class="message">'



with open('message.json') as f:
  with open('messages.txt', 'w') as out:
    data = json.load(f)
    for msg in data["messages"]:
      if msg["sender_name"] == 'Sarina Carter' and 'content' in msg.keys():
        print(msg)
        out.write(msg["content"] + "\n")


# with open('602.html') as f:
#   searched = []
#   for line in f.readlines():
#     regex = re.compile(fbMessageRegex)
#     searched += regex.findall(line)
#     print(len(searched))
#   with open('dereks_messages.txt', 'w') as out:
#     for s in list(map(lambda x: x[1], searched)):
#       out.write(str(s) + "\n")