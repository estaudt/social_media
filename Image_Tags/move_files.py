import os
import glob
import shutil
import math
from nltk.corpus import wordnet as wn
#from nltk import word_tokenize
#from nltk import pos_tag

word_list = ['castle','foot','man','face','tower','waterfall','statue','moon','apple','heart','blossom','lamp','truck','bunny','rabbit','bear','person','lion','portrait','sunset','street','beach','tree','girl','bird','woman','graffiti','dog','building','car','window','plant','train','mountain','cloud','baby','insect','boy','horse','kitty','eye','cake','bus','cactus','ball','lion','monkey','tiger','palm','goose']

tagsDir = '/Users/elliotstaudt/Documents/MIRFLICKR/tags/'
#newTagsDir = '/Users/elliotstaudt/Documents/MIRFLICKR/tags_new/'
newTagsDir = '/Users/elliotstaudt/Documents/MIRFLICKR/tags_new_2/'
imageDir = '/Users/elliotstaudt/Documents/MIRFLICKR/images/'
gistDir = '/Users/elliotstaudt/Documents/MIRFLICKR/features_gist/'
newGistDir = '/Users/elliotstaudt/Documents/MIRFLICKR/features_gist_new/'

first = False

# look through the image folder and copy all tags and gist descriptors associated with the files within.
image_file_names = glob.glob(imageDir+'*.jpg')
for image_file in image_file_names:
  (head,tail)=os.path.split(image_file)
  (fname,ext)=os.path.splitext(tail)
  fldrNum = str(int(math.floor(int(fname)/10000)))
  
  # create new tag file
  src_tag = os.path.join(tagsDir,fldrNum,fname+'.txt')
  dst_tag = os.path.join(newTagsDir,fname+'.txt')
  with open(src_tag) as f:
    content = [x.strip('\n') for x in f.readlines()]
    content = [x.strip('\r') for x in content]
    
  sf = open(dst_tag, 'w')
  
  first = True
  for word in content:
    # check to see the word is ascii encoded
    try:
      word = word.decode('ascii')
    except UnicodeDecodeError:
      continue
    # word is ascii encoded so attempt to find the synonym
    syn = wn.morphy(word)
    if syn in word_list:
      if first:
        sf.write(syn)
        first = False
        continue
      sf.write('\n')
      sf.write(syn)
        
  sf.close();

  # copy gist file
  src_gist = os.path.join(gistDir,fldrNum,fname+'.dat')
  dst_gist = os.path.join(newGistDir,fname+'.dat')
  shutil.copy(src_gist, dst_gist)

print('fin')