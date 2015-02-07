import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
import glob
import collections
import sparsipy


cluster_filename = '/Users/elliotstaudt/Documents/MIRFLICKR-25000/Clusters/BOW_200_clusters.mat'

# Create the blank dictionary that will hold word associations for all object types


# Load assignments from clustering BoW descriptors for each object
f = sio.loadmat(cluster_filename)

assignments = np.array(f['assignments'])
centers = np.array(f['centers'])

print assignments.shape
print centers.shape[1]


master_dict = dict()
cluster_dicts = [collections.OrderedDict() for x in range(centers.shape[1])]
print len(cluster_dicts)

tagsDir = '/Users/elliotstaudt/Documents/MIRFLICKR-25000/tags/'
objectsDir = '/Users/elliotstaudt/Documents/MIRFLICKR-25000/objects/'
# Get the names of each of the processed tag files in the tag directory.
# Read the tags and find the synonym for each one, if one exists.
for num in range(25000):
  # establish name of the synonym file
  fname = tagsDir + str(num) + '_synonyms.txt'
  # open the synonym file and read the contents into a list
  with open(fname) as f:
    content = [x.strip('\n') for x in f.readlines()]
    content = [x.strip('\r') for x in content]

  for word in content:
    if word not in master_dict:
      master_dict[word] = 0

# create an ordered dictionary
master_dict_ordered = collections.OrderedDict(sorted(master_dict.items(), key=lambda t: t[0]))
# Set all dictionary in cluster_dicts equal to the blank master dictionary
for key in master_dict_ordered:
  for x in range(centers.shape[1]):
    cluster_dicts[x][key] = 0


# start associating object classes to tags
for ind in range(5):
  
for num in range(25000):
  # establish name of the synonym file
  fname = tagsDir + str(num) + '_synonyms.txt'
  # open the synonym file and read the contents into a list
  with open(fname) as f:
    content = [x.strip('\n') for x in f.readlines()]
    content = [x.strip('\r') for x in content]
  # get then names of the object files associated with the tag file
  local_object_files = glob.glob(objectsDir+str(num).zfill(5)+'/objClass_200_5k'+'*.mat')
  if len(local_object_files) > 0:
    for count in range(len(local_object_files)):
      index_file = sio.loadmat(local_object_files[count])
      object_index = index_file['index']-1
      # now go through the tags and increment the appropriate location in dictionary list
      for word in content:
        cluster_dicts[object_index][word] += 1

# Create a matrix that corresponds to cluster-word matches
word_matches = np.zeros((len(cluster_dicts),len(master_dict_ordered.keys())))
for num in range(len(cluster_dicts)):
  key_count = 0 #keep track of the keys
  for key in cluster_dicts[num]:
    word_matches[num,key_count] = cluster_dicts[num][key]
    key_count+=1
  
# Save the tags associated with objects to their own file
object_class_Dir = '/Users/elliotstaudt/Documents/MIRFLICKR/tag_associations/200_words_5k'+str(ind)+'/'
lambda_ = 0.094
num_words = 10;
keys = master_dict_ordered.keys()
object_words = []
for num in range(len(cluster_dicts)):
#for num in range(1):
  a = word_matches[num,:]
  #ind = np.argpartition(a, -10)[-10:]
  inds = sparsipy.sparsify(a, lambda_, 1)
  
  print num
  fsavename = object_class_Dir + str(num) + '.txt'
  sf = open(fsavename,'w')
  local_count = 0
  for index in range(len(inds)):
    if local_count != 0:
      sf.write('\n')
    local_count += 1
    #matched_word = keys[ind[index]]
    matched_word = keys[inds[index]]
    sf.write(matched_word)
  sf.close()
  print len(inds)



