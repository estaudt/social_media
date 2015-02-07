import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import os
import glob
import collections
import sparsipy
from nltk.corpus import wordnet as wn
from nltk import word_tokenize
from nltk import pos_tag


master_dict = dict()
tagsDir = '/Users/elliotstaudt/Documents/tags/'

first = False
tag_folders = glob.glob(tagsDir)
for num in range(100):
  print num
  tag_file_names = glob.glob(tagsDir+str(num)+'/*.txt')
  for tagFile in tag_file_names:
    # open the tag file and read the contents into a list
    # strip each line of newline character and raw character
    with open(tagFile) as f:
      content = [x.strip('\n') for x in f.readlines()]
      content = [x.strip('\r') for x in content]
      
    # check to make sure the list isn't zero length
    if len(content) == 0:
      continue
    
    # process each word in the list
    for word in content:
      # try to decode into ascii
      # if it fails, skip the word
      try:
        word = word.decode('ascii')
      except UnicodeDecodeError:
        continue
    # word is ascii encoded so attempt to find the synonym
      syn = wn.morphy(word)
      if syn != None and len(syn) > 2:
        # a synonym was found, so confirm it is a basic noun
        text = word_tokenize(word)
        token = pos_tag(text)
        if token[0][1] == 'NN':
          # it was a proper noun so include in the dictionary
          if syn in master_dict:
            master_dict[syn] += 1
          else:
            master_dict[syn] = 1

# sort by value (word count)
master_dict_ordered = collections.OrderedDict(sorted(master_dict.items(), key=lambda t: t[1]))

first = True
keys = master_dict_ordered.keys()
sf = open('/Users/elliotstaudt/Documents/ordered_tags.txt', 'w')
for tag in reversed(keys):
  if first:
    sf.write(tag)
    first = False
    continue
  sf.write('\n')
  sf.write(tag)
sf.close()