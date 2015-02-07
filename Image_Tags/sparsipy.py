import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.io as sio
from nltk.corpus import wordnet as wn
from nltk import word_tokenize
from nltk import pos_tag
import collections
import random
import math

def sparsify(a, lambda_, dist_type):
  cols = []
  vals = np.array(a)
  cover = vals*0
  sort_index = np.argsort(vals)
  min_dist = np.linalg.norm(vals)
  min_ind = len(a)
  '''
  count = 0
  for ind in reversed(sort_index):
    cover[ind] = vals[ind]
    vals[ind] = 0
    temp_dist = np.linalg.norm(vals) + lambda_*np.linalg.norm(cover,dist_type)
    if temp_dist < min_dist:
      min_dist = temp_dist
      min_ind = count
  '''
  for count in range(len(a)):
    cover[sort_index[-1-count]]=vals[sort_index[-1-count]]
    vals[sort_index[-1-count]] = 0
    temp_dist = np.linalg.norm(vals) + lambda_*np.linalg.norm(cover, dist_type)
    if temp_dist < min_dist:
      min_dist = temp_dist
      min_ind = count+1
  
  for count in range(min_ind):
    cols.append(sort_index[-1-count])

  return np.array(cols)


def convertToSynonyms(fname, excluded_words = []):
  with open(fname) as f:
    content = [x.strip('\n') for x in f.readlines()]
    content = [x.strip('\r') for x in content]
  
  # define file in which to store synonyms
  # [root,ext]=os.path.splitext(fname)
  [path,file]=os.path.split(fname)
  [path,junk]=os.path.split(path)
  fsavename = os.path.join(path,"synonyms",file)
  
  # open file for writing
  sf = open(fsavename, 'w')
  
  first = True
  for word in content:
    # check to see the word is ascii encoded
    try:
      word = word.decode('ascii')
    except UnicodeDecodeError:
      continue
    # word is ascii encoded so attempt to find the synonym
    syn = wn.morphy(word)
    if syn != None and len(syn) > 2 and syn not in excluded_words:
      # a synonym was found, so confirm it was a basic noun
      text = word_tokenize(word)
      token = pos_tag(text)
      if token[0][1] == 'NN':
        # it was a proper noun so write it to the file
        if first:
          sf.write(syn)
          first = False
          continue
        sf.write('\n')
        sf.write(syn)

  # close the file for writing
  sf.close()


def drawHistogram(data, numBins):
  # the histogram of the data
  n, bins, patches = plt.hist(data, numBins, facecolor='blue', alpha=0.75)
  
  plt.xlabel('Word Counts')
  plt.ylabel('Number of Words with Count in Range')
  plt.title(r'$\mathrm{Histogram\ of\ Word\ Counts\ with\ %i\ Words}$'%(len(data)))
  #plt.axis([40, 160, 0, 0.03])
  plt.grid(True)
  
  plt.show()


def drawDictValues(values):
  values.sort()
  plt.plot(range(len(values)),values,linewidth=2)
  plt.xlabel(r'$\mathrm{Words\ from\ Least\ Represented\ to\ Most}$')
  plt.ylabel(r'$\mathrm{Word\ Counts}$')
  plt.title(r'$\mathrm{Word\ Counts\ of\ %i\ Words}$'%(len(values)))
  
  plt.show()


def buildTagClusterAssociation(index_file_names, tag_dir, words, num_centers, excluded_min, excluded_max):
  # Inputs --
  # words:       a previously determined list 
  #              words we are expecting to find
  # num_centers: the number of cluster centers
  #              used in clustering
  # Outputs --
  # returns numpy matrix of centroids by words with word counts

  # define object to hold tag-to-centroid count
  cluster_dicts = [collections.OrderedDict() for x in range(num_centers)]
  # seed the word values to each of the dictionaries
  for word in words:
    for x in range(num_centers):
      cluster_dicts[x][word] = 0
  
  #for num in range(len(index_file_names)):
  # go through each index file and update that index with it's associated tags
  index_count = 0;
  for index_file in index_file_names:
    if index_count >= excluded_min and index_count < excluded_max:
      index_count +=1
      continue
    index_count+1
    # get the pro
    index = sio.loadmat(index_file)
    object_index = index['index']-1
    
    # establish name of the synonym file
    (head,tail)=os.path.split(index_file)
    (fname,ext)=os.path.splitext(tail)
    tfname = os.path.join(tag_dir,fname+'.txt')
    
    # open the tag file and read the contents into a list
    with open(tfname) as f:
      content = [x.strip('\n') for x in f.readlines()]
      content = [x.strip('\r') for x in content]
    
    # go through the contents of the tag file and update word count for that index
    for word in content:
      cluster_dicts[object_index][word] += 1
  
  word_matches = np.zeros((num_centers,len(words)))
  for num in range(num_centers):
    key_count = 0 # have to count the number of keys for the proper 
    for key in cluster_dicts[num]:
      word_matches[num,key_count] = cluster_dicts[num][key]
      key_count+=1
  
  return word_matches


def matrixToTagAssociationList(index_file_names,tag_dir,tag_clusters_dir,num_centers,excluded_min,excluded_max):
  # list to hold results
  matchings = [0.0 for num in range(10)]
  # open tag-cluster files and read them into a large list
  cluster_words = []
  for num in range(num_centers):
    cluster_name = os.path.join(tag_clusters_dir,str(num)+'.txt')
    with open(cluster_name) as c:
      content = [x.strip('\n') for x in c.readlines()]
      content = [x.strip('\r') for x in content]
    if len(content) > 10:
      cluster_words.append(content[0:10])
    else:
      cluster_words.append(content)
  
  # open index files of excluded objects
  index_count = 0;
  for index_file in index_file_names:
    if index_count < excluded_min or index_count >= excluded_max:
      index_count +=1
      continue
    index_count +=1
    # get the pro
    index = sio.loadmat(index_file)
    object_index = index['index']-1
    
    # establish name of the synonym file
    (head,tail)=os.path.split(index_file)
    (fname,ext)=os.path.splitext(tail)
    tfname = os.path.join(tag_dir,fname+'.txt')
    
    # open the tag file and read the contents into a list
    with open(tfname) as f:
      content = [x.strip('\n') for x in f.readlines()]
      content = [x.strip('\r') for x in content]
    
    # check specifically which index is matched
    cluster = cluster_words[object_index]
    clust_count = 0
    for word in cluster:
      if word in content:
        matchings[clust_count] += 1
        break
      clust_count +=1
    
  return matchings

def randomMatchings(index_file_names,tag_dir,num_centers,excluded_min,excluded_max):
    # list to hold results
  matchings = [0.0 for num in range(10)]
  
  # define the the index files that will comprise the random groupings
  index_file_names_rand = []
  if excluded_min == 0:
    index_file_names_rand.extend(index_file_names[excluded_max:len(index_file_names)])
  elif excluded_max == len(index_file_names):
    index_file_names_rand.extend(index_file_names[0:excluded_min])
  else:
    index_file_names_rand.extend(index_file_names[0:excluded_min])
    index_file_names_rand.extend(index_file_names[excluded_max:len(index_file_names)])
  
  # randomize the list and make new clusters
  random.shuffle(index_file_names_rand)
  numelems = len(index_file_names_rand)
  step = int(math.ceil(float(numelems)/num_centers))
  partitions = range(num_centers+1)
  partitions = [step*num for num in partitions]
  if partitions[-1] != numelems:
    partitions[-1] = numelems
  
  # open the files
  cluster_words = [];
  for num in range(num_centers):
    cluster = []
    temp_dict = dict()
    for count in range(partitions[num],partitions[num+1]):
      # establish name of tag file
      (head,tail)=os.path.split(index_file_names_rand[count])
      (fname,ext)=os.path.splitext(tail)
      tfname = os.path.join(tag_dir,fname+'.txt')
      
      # open the tag file and read the contents into a list
      with open(tfname) as f:
        content = [x.strip('\n') for x in f.readlines()]
        content = [x.strip('\r') for x in content]
      
      # add words to dictionary
      for word in content:
        if word in temp_dict:
          temp_dict[word] += 1
        else:
          temp_dict[word] = 1
      
    # dictionary is populated, time to sort
    temp_dict = collections.OrderedDict(sorted(temp_dict.items(),key=lambda t: t[1]))
    keys = temp_dict.keys()
    for count in range(10):
      cluster.append(keys[-1-count])
    cluster_words.append(cluster)
  
  # open index files of excluded objects
  index_count = 0;
  for index_file in index_file_names:
    if index_count < excluded_min or index_count >= excluded_max:
      index_count +=1
      continue
    index_count +=1
    # get the pro
    index = sio.loadmat(index_file)
    object_index = index['index']-1
    
    # establish name of the synonym file
    (head,tail)=os.path.split(index_file)
    (fname,ext)=os.path.splitext(tail)
    tfname = os.path.join(tag_dir,fname+'.txt')
    
    # open the tag file and read the contents into a list
    with open(tfname) as f:
      content = [x.strip('\n') for x in f.readlines()]
      content = [x.strip('\r') for x in content]
    
    cluster = cluster_words[object_index]
    clust_count = 0;
    for word in cluster:
      if word in content:
        matchings[clust_count] += 1
        break
      clust_count += 1
    
  return matchings
  