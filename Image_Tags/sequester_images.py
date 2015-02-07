# Look in all tag files
# match against word list
# if match, copy image and move it into image file

#import numpy as np
#import matplotlib.pyplot as plt
import os
import glob
import shutil
import math
from nltk.corpus import wordnet as wn
#from nltk import word_tokenize
#from nltk import pos_tag

word_list = ['castle','foot','man','face','tower','waterfall','statue','moon','apple','heart','blossom','lamp','truck','bunny','rabbit','bear','person','lion','portrait','sunset','street','beach','tree','girl','bird','woman','graffiti','dog','building','car','window','plant','train','mountain','cloud','baby','insect','boy','horse','kitty','eye','cake','bus','cactus','ball','lion','monkey','tiger','palm','goose']

tagsDir = '/Users/elliotstaudt/Documents/MIRFLICKR/tags/'
imageDir = '/Users/elliotstaudt/Documents/MIRFLICKR/images'

first = False

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
      if syn in word_list:
        (head,tail)=os.path.split(tagFile)
        (fname,ext)=os.path.splitext(tail)
        fldrNum = str(int(math.floor(num/10)))
        src_image = os.path.join(imageDir+fldrNum,str(num),fname+'.jpg')
        dst_image = os.path.join(imageDir,fname+'.jpg')
        shutil.copy(src_image, dst_image)
        continue

