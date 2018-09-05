from numpy.random import choice
import pickle
import sys
from collections import deque
import time

class markov_node:
  def __init__(self, word=None):
    self.word = word
    self.nextWords = list()
    self.nextCounts = list()

  def getNext(self):
    total = sum(self.nextCounts)
    percents = list(map(lambda x: float(x)/total, self.nextCounts))
    return choice(self.nextWords, p=percents)
  
  def addCount(self, word):
    try:
      index = self.nextWords.index(word)
      self.nextCounts[index] += 1
    except ValueError:
      self.nextWords.append(word)
      self.nextCounts.append(1)
    
  def __str__(self):
    both = list(zip(self.nextWords, self.nextCounts))
    mapping = {}
    for nw, nc in both:
      mapping[nw] = nc
    return str(self.word) + " " + str(mapping)


def wordExists(nodelist, word):
  wordlist = list(map(lambda x: x.word, nodelist))
  try:
    return nodelist[wordlist.index(word)]
  except ValueError:
    return False

def train(filename):
  nodelist = deque()
  nodelist.append(markov_node([" ", " "]))
  with open(filename, 'r', encoding="utf-8") as f:
    count = 0
    lines = f.readlines()
    total = len(lines)
    made = set()
    made.add(str.encode("  ", 'utf-8'))
    start = 0
    for line in lines:
      count += 1
      if count%1000 == 0:
        print(int(round(time.time() * 1000))-start)
        start = int(round(time.time() * 1000))
      if not line.startswith("RT") and not line.startswith("http"):
        prev = " "
        prev2 = " "
        node = nodelist[0]
        for curr in line.lower().strip().replace("\n", " ").split(" "):
          if not curr.startswith("RT") and not curr.startswith("http") and curr is not "":
            if node:
              node.addCount(curr)
              lastnode = node
            else:
              newNode = markov_node([prev2, prev])
              made.add(str.encode(prev2 + prev, 'utf-8'))
              newNode.addCount(curr)
              nodelist.append(newNode)
              lastnode = newNode

            if str.encode(prev + curr, 'utf-8') in made:
              node = nodelist[list(made).index(str.encode(prev2 + prev, 'utf-8'))]
            else:
              node = False
            prev2 = prev
            prev = curr
        lastnode.addCount("\n")
  with open('messages.pkl', 'wb') as pickle_file:
    pickle.dump(nodelist, pickle_file)
  return nodelist

def create(nodelist, seed):
  # node = wordExists(nodelist, seed)
  node = choice(nodelist)
  tweet = ""
  if node:
    nextWord = node.getNext()
    while node:
      nextWord = node.getNext()
      tweet += node.word[1] + " "
      nextPair = [node.word[1], nextWord]
      node = wordExists(nodelist, nextPair)
    tweet += nextWord
    # if tweet.count(" "):
    #   return create(nodelist, seed)
    print(tweet)
  
if len(sys.argv) == 1:
  nodelist = train("messages.txt")
else:
  with open('messages.pkl', 'rb') as pickle_file:
    nodelist = pickle.load(pickle_file)
    for i in range(20):
      create(nodelist, [" ", " "])