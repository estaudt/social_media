import numpy as np
import scipy.io as sio
import os
import glob
import scipy.linalg as linalg
import sparsipy
import math

num_clusters = 10;
lambda_ = 0.1
index_dir = '/Users/elliotstaudt/Documents/MIRFLICKR/clusters/'+str(num_clusters)
tag_dir = '/Users/elliotstaudt/Documents/MIRFLICKR/tags_new'

word_list = ['castle','foot','man','face','tower','waterfall','statue',\
             'moon','apple','heart','blossom','lamp','truck','bunny',\
             'rabbit','bear','person','portrait','sunset','street',\
             'beach','tree','girl','bird','woman','graffiti','dog',\
             'building','car','window','plant','train','mountain','cloud',\
             'baby','insect','boy','horse','kitty','eye','cake','bus',\
             'cactus','ball','lion','monkey','tiger','palm','goose']

# establish different groups
index_file_names = glob.glob(os.path.join(index_dir,str(1),'*.mat'))
numelems = len(index_file_names)
step = int(math.ceil(float(numelems)/5))
exclude = range(6)
exclude = [step*num for num in exclude]
if exclude[-1] != numelems:
  exclude[-1] = numelems

# Read the objects that weren't used to create cluster-tag associations and test
for num in range(1,6):
  print 'Matchings for group', num
  # grab index names
  index_file_names = glob.glob(os.path.join(index_dir,str(num),'*.mat'))
  
  # get proper tag cluster directory name
  tag_clusters_dir = os.path.join(index_dir,str(num),'tag_clusters')
  
  matchings = []
  matchings = sparsipy.matrixToTagAssociationList(index_file_names,tag_dir,tag_clusters_dir,\
                                                  num_clusters,exclude[num-1],exclude[num])
  
  #print [matchings[trash]/(exclude(num)-exclude(num-1)) for trash in range(10)]
  print matchings
print 'fin'