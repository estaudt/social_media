import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import os
import glob
import collections
import sparsipy
import math


num_clusters = 400;
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
if exclude[-1] != numelems+1:
  exclude[-1] = numelems+1

# Create a matrix that corresponds to cluster-word matches and
# print most significant words of each group to a file. Do this
# for each division of the main group
for num in range(1,6):
  print 'Finding tag-cluster associations for iteration:', num
  
  index_file_names = glob.glob(os.path.join(index_dir,str(num),'*.mat'))
  num_indexes = len(index_file_names)
  
  # get word matches to clusters
  word_matches = sparsipy.buildTagClusterAssociation( index_file_names, tag_dir, word_list, \
                                                      num_clusters, exclude[num-1], exclude[num])

  # Define folder in which to save the tags associated with clusters
  tag_clusters_dir = os.path.join(index_dir,str(num),'tag_clusters')

  # find the most significant words for each cluster and print them to a file
  print 'Printing words to files'
  object_words = []
  for cluster in range(num_clusters):
    a = word_matches[cluster,:]
    inds = sparsipy.sparsify(a, lambda_, 1)
    
    fsavename = os.path.join(tag_clusters_dir, str(cluster) + '.txt')
    sf = open(fsavename,'w')
    local_count = 0
    for index in range(len(inds)):
      if local_count != 0:
        sf.write('\n')
      local_count += 1
      #matched_word = keys[ind[index]]
      matched_word = word_list[inds[index]]
      sf.write(matched_word)
    sf.close()
  
print 'fin'
