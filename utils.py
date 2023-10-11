#  UTILS:
import os 
from functools import partial   
from pathlib import Path     
from PIL import Image, ImageEnhance 
#from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np  
from scipy import ndimage
#from scipy import ndimage as ndi
import random
#from random import randint, seed, randrange, uniform, sample

import matplotlib.pyplot as plt
import csv
     
#from prettytable import PrettyTable
#mport matplotlib.colors
#from matplotlib.colors import ListedColormap
import pandas as pd     
import shutil 
import time
#import re      
    
import pickle

from skimage.io import imread 


from skimage.measure import label, regionprops
import glob    
from natsort import natsorted





####  ===========  [1]
#=====>  preprocessing_py:

def make_folders(root_directory, filenames):
  concat_root_path = partial(os.path.join, root_directory)
  make_directory = partial(os.makedirs, exist_ok=True)
  for path_items in map(concat_root_path, filenames):
    make_directory(path_items)  
  print(f'Folders were succesfully created!')
  return True  

def make_list_file(mypath):  

  onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
  return onlyfiles 

# create a csv file para os detalhes  de cada filename
def pclass_lista(L_filenames, dir_, nclass_, 
                 saved_filename=None):
  N = nclass_    
  Lista=[[] for i in range(N+1)]  

  for imgs in L_filenames:
    im=Image.open(dir_ + imgs)
    
    for i in range(N+1):
      count= sum(im.point(lambda pix: 1 if pix== i else 0).getdata())
      Lista[i].append(count)

  objs = {'Filenames':L_filenames, 'c0': Lista[0], 'c1': Lista[1], 
          'c2':Lista[2], 'c3': Lista[3],
         'c4': Lista[4], 'c5':Lista[5], 
          'c6':Lista[6]}
    
  
  df = pd.DataFrame(objs)     
  if  saved_filename is not None: 
    df.to_csv(saved_filename, index=False)
  else:
    pass    

  return df  
   
def label_to_binary_(im_arr, _class):#, threshold):
  binarr=np.where(im_arr== int(_class), 1,0)
  bb=binarr*255  
  binarr= bb.astype(np.uint8)        
  return Image.fromarray(binarr)
 

def binary_per_class_(in_path, path_save, Lista_targets):
  #  create mask per class  from  palette image
  # pathfile is a path of palette images are.    

  for  file in Lista_targets: 
    im=Image.open(in_path + file)#.convert('L')  
    im_arr=np.asarray(im)
    #list_class =  np.unique(im_arr)    
    _ , counts = np.unique(im_arr, return_counts=True)

    counts = counts.tolist()  
 
          
    list_nclass = [counts.index(item)  for item in counts[1:] if item > 121]#Treshold0]
    #counts.index(item) + 1  for item in counts if item > 9]
    #print('List_nclass:>>', list_nclass)
    #list_nclass = [list_class[i] for i in item.index if ]
    for n in list_nclass:
      nbase0 = file.split('.')[0]
      nbase = nbase0 + "_" + str(n) + ".png"

      out_class=label_to_binary_(im_arr, n) 
      out_class.save(path_save+ nbase, 'PNG')

  return True 

def  quartiles_x(filenames, dir_,  nclasses,
                  percentile):        
  Lista_areas_=[[]  for i in range(nclasses)]
  NLabels= 0  
  for file_ in filenames:
    nclass_ = file_.split('.')[0][-1]
    img= imread(dir_ + file_)
    labels = label(img)
    phases = regionprops(labels)         
    Label_area=[]
    
    for region in phases:
      Label_area.append(region.area)
    i=  int(nclass_) - 1
    Lista_areas_[i]+= Label_area
    nLabel= labels.max()
    NLabels += nLabel

  QUARTILE = [int(np.percentile(Lista_areas_[i], percentile)) for i in range(nclasses)]                                                               
  return  QUARTILE 


#===========   [2]
#==============> gen_annotations.py
def SaveLists(data, name_file_pkl):# name_file  sem extension
    open_file = open(name_file_pkl,"wb")
    pickle.dump(data, open_file)
    open_file.close()

def LoadLists(filepath):    
    open_file = open(filepath, "rb")
    loaded_list = pickle.load(open_file)
    open_file.close()
    return loaded_list  

# write list to binary file
def write_list(alist, nome_file_path):
    # store list in binary file so 'wb' mode
    with open(nome_file_path, 'wb') as fp:
        pickle.dump(alist, fp)
        print('Done writing list into a binary file')  


# Create color palette from color dictionary
def palette_from_dict(c_dict):
    palette = []
    for i in np.arange(256):
        if i in c_dict:
            palette.extend(c_dict[i])  
        else:
            palette.extend([0, 0, 0])
    return palette  


#  =========================
#  =========    gen_imgs_1class.py

def make_img_bg(_mean_std_bg, img_size):
  
  sample = random.choice(_mean_std_bg)
  info_mean, info_std = sample[0], sample[1]
  randomnumber = round(random.normalvariate(info_mean, info_std))
  
  new_im = Image.new(mode='L', size=img_size)

  for x in range(img_size[0]):
    for y in range(img_size[1]):
      new_im.putpixel((x, y), randomnumber)

  return new_im  

def gen_imgs_pd_i(pd_dict_i, Lista_i):

  #filtra  o pandas  só os index (filename )  de interesse:

  #Lindex = pd_dict_i.index.tolist()
  #new_ ==[itm  for itm in Lindex if itm not in Lista_except_i]  
  pdi = pd_dict_i[pd_dict_i.index.isin(Lista_i)]  
    
  return pdi 


#  =================  
#  =======    multiple_annotations.py 


def pandas_sorted_by_columns(pd_):
    #pd_ = pd.read_csv(filepath_pd_in)
  cols_df = pd_.columns.tolist() 
  df_sorted_by_column= pd.DataFrame() 

  for j in range(len(pd_.columns)):
    col = cols_df[j]    
    L1 = pd_.loc[:,col].tolist()
    L11 = random.sample(L1, len(L1))  
    df_sorted_by_column[col]= L11   
            
  return df_sorted_by_column  


def Ldir_plots(Lista_mk): #Lista_mask
  
  n0 = len(Lista_mk) # Lista_mi
  nList_ = [[] for i in range(n0)]
  for i in range(n0):  
    L01 = Lista_mk[i].split('.')[:-1]
    L1 = [item + '.png' for item in L01]
    nList_[i]=L1

  return nList_      


def nested_List_flatten(Lista_mk): # Lista_  = nested_List_flatten(Lista_mk)Lista_mk

  #Function to help to flatten a nested list.

  List_Lk = Ldir_plots(Lista_mk)
  return [item for sublist in List_Lk for item in sublist]

#======================  
# =  gen_imgs_nclasses.py


def split_filenames_per_class(Listx,nclass):
  new_List = [[] for i in range(nclass)]  
  for fname in Listx:
    #print('fname::>>', fname)
    c = fname.split('.')[0][-1]
    #print('c1::>>', c)  
    #c = int(fname.split('.')[0][-1])
    new_List[int(c)-1] +=[fname]

  return new_List  

def filter_pd_(pd_, List_of_values):
  #df[df['A'] in list_of_values]
  new_pd_ = pd_[pd_['Lfilename'].isin(List_of_values)]   

  return new_pd_  

#  ===========
#  ============>

# =============   gen_missing_imgs.py


print('The end of UTILS_.PY')
       
