#  UTILS:
import os 
from functools import partial   
from pathlib import Path     
    
#from skimage.util import random_noise
   
from PIL import Image, ImageFilter
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np  
from scipy import ndimage
from scipy import ndimage as ndi
from random import randint, seed, randrange, uniform

import matplotlib.pyplot as plt
import csv
     
#from prettytable import PrettyTable
import matplotlib.colors
from matplotlib.colors import ListedColormap
import pandas as pd  
import random    
import shutil 
import datetime
import time
from functools import partial
import re      
   

    
import pickle
   
from skimage.morphology import disk
from skimage.filters import median
from skimage.io import imread 
from skimage.filters import sobel
from PIL import Image, ImageEnhance     
#import skimage.io
from skimage.measure import label, regionprops, regionprops_table
from skimage.transform import rotate
import glob    
from natsort import natsorted

from random import sample   
        


def random_bg(arr_bg):
  info_mean = np.mean(arr_bg)
  info_std = np.std(arr_bg)
  return round(random.normalvariate(info_mean, info_std))
     

"""  
def _cmap():
  color_map1=['#000000', #background   - 0  
            '#D90B3B',#'#FF003C', #rojo - 1  
            '#4BC509',  #5BFA05': verde - 2
            '#C3B35A',# '#E0C94A', amarlllo - 3    
            '#0C0588',# '#0D00FA',azul - 4    
            '#A61D9B',#'#E65CDB', fucsia - 5 
            '#4DAF8D'] #  '#51E0AE'] turquesa - 6

  return matplotlib.colors.ListedColormap(color_map1) 

"""


palette =[ 
        0,0,0, #negro  
        217,11,59, #rojo  
        75, 197, 9, # verde    
        195, 179, 90, #amarillo
        12, 5, 136, #azul  
        166, 29, 155, #fucsia
        77, 175, 141, #turquesa  
        ] 

colors_dict = { 0: [0,0,0], 1: [217,11,59], 2:[75, 197, 9], 
                  3: [195, 179, 90], 4: [12, 5, 136], 
                  5:[166, 29, 155], 6: [77, 175, 141],
                  }







def make_list_file(mypath):  

  onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
  return onlyfiles 
    
#X
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
   



def make_folders_class(root_directory, filenames):
    concat_root_path = partial(os.path.join, root_directory)
    make_directory = partial(os.makedirs, exist_ok=True)
    for path_items in map(concat_root_path, filenames):
      make_directory(path_items)  
    print(f'Folders were succesfully created!')
    return True  


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
    #print(counts)    
          
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
  

# Create color palette from color dictionary
def palette_from_dict(c_dict):
    palette = []
    for i in np.arange(256):
        if i in c_dict:
            palette.extend(c_dict[i])  
        else:
            palette.extend([0, 0, 0])
    return palette  


def renome_filenames_path(folder_in, str_, ext):

  filelist= [file for file in os.listdir(folder_in) if file.endswith('.'+ ext)]
  for file_ in filelist:
    old_name = folder_in + file_
    new_name = folder_in +  file_.split('.')[0] + str_ +'.'+ ext
    # enclosing inside try-except
    try:
        os.rename(old_name, new_name)  
    except FileExistsError:
        # skip the below code
        # if you don't' want to forcefully rename
        os.remove(new_name)
        # rename it
        os.rename(old_name, new_name)

  print("Files are all  renomed  successfully") 
  return True    

def copy_files_dir_to_dir(origin, target, remove=True):

    # Fetching the list of all the files  
    _files = [f for f in os.listdir(origin) if os.path.isfile(os.path.join(origin, f))]

    # Fetching all the files to directory
    for file_name in _files:  
        shutil.copy(origin+file_name, target+file_name)

        if remove:
          os.remove(origin+file_name)

        else:  
   
          continue
    print("Files are copied successfully")   
    return True

def making_needed_paths(folders, _PATH):
  """
  #  ======   Define all needed path:
  #python program to check if a directory exists
  """  
   
  for folder in folders:
      full_path = os.path.join(_PATH, folder)#output_files_path,folder)
      if not os.path.exists(full_path):
          print('Creating folders...')
          os.makedirs(full_path)
      else:
        #print('The directory {} is present.'.format(full_path))
        pass
  print('All  folders were created...')
  return True
    
def make_img_masks2(bg_dir,in_binary,input_dir, out_dir, Lista_inputs):#, T):

  # in_dir is a path from mask images
  # out_dir is a path where is saved
  bg = Image.open(bg_dir + 'background.jpg')
  for file_ in Lista_inputs:
      mask= Image.open(in_binary + file_)
      base2 = file_.split('_',1)[1].split('.')[0][:-2]     
      img= Image.open(input_dir + base2 + '.jpg')
      output= Image.composite(img, bg, mask)
      new_fname=  out_dir  +  file_.split('_',1)[1].split('.')[0] + '.jpg'
      output.save(new_fname)  
          
  return True        

  
def sum_pixels_in_targets(folder_target, nclass):
  Lista_class=[i for i in range(nclass+1)]
  SUMx = np.zeros(7)
  filenames = make_list_file(folder_target)

  for file_ in filenames:
    #print('FIle de analise:', file_)
    img= Image.open(folder_target + file_)
    im_arr = np.asarray(img)
    colors, counts = np.unique(im_arr.flatten(),  
                           return_counts = True, 
                           axis = 0)

    Soma = [0 for i in range(nclass +1)]
    for i in range(len(colors)):
      #print('value i:', i) 
      idx=colors[i]

      Soma[idx] +=counts[i]

    SUMx +=np.array(Soma)
  return SUMx.astype(int)


def make_folders(root_directory, filenames):
  concat_root_path = partial(os.path.join, root_directory)
  make_directory = partial(os.makedirs, exist_ok=True)
  for path_items in map(concat_root_path, filenames):
    make_directory(path_items)  
  print(f'Folders were succesfully created!')
  return True  
     


def  verify_(nclass, dir_img, dir_target, Nimgs):
  """ 
  Verify  amount files into folders imgs and labels:

  """
  for i in range(nclass):
    print('=======')
    print('CLASS {}'.format(i+1))
    if Nimgs[i]==len(make_list_file(dir_img[i])):
      print('All images of class {} were created in folder {}'.format(i+1, dir_img[i]))
      if Nimgs[i]== len(make_list_file(dir_target[i])):
        print('All images masks  of class {} were created in folder {}'.format(i+1, dir_img[i]))

      else:
        print('Trouble in creating mask images of class {}'.format(i+1))

    else:
      print('Trouble in creating images of class {}...'.format(i+1))
    
  return True

def make_folders(root_directory, filenames):
  concat_root_path = partial(os.path.join, root_directory)
  make_directory = partial(os.makedirs, exist_ok=True)
  for path_items in map(concat_root_path, filenames):
    make_directory(path_items)  
  print(f'Folders were succesfully created!')
  return True  
   
def verify_masked(Lnumber_imgs, nclass, folder): 
  """ 
  function which verify amount images masked generated  in folder 
  """
  for k in range(nclass):
    Lista_k= len(make_list_file(folder[k]))
    print(Lnumber_imgs[k]==Lista_k)

def making_pd_fn3(pwd, M, nclass):
  """     
  function to help the construction of table dataframe  
  where all columns correspond the filename per class of Lista_to_remove
  """
  df_empty = pd.DataFrame(index=range(0,M), dtype = 'str')
  csv_files = glob.glob(os.path.join(pwd, "*.csv"))

  for file_ in csv_files:
    dfx = pd.read_csv(file_, usecols=['Lfilename']).fillna(0)  
    ffname = file_.split('.')[0]
    name_col = 'classe'+str(ffname[-1])
    dfx.columns = [name_col]
    df_empty = pd.concat([df_empty, dfx], axis=1)

    df_empty = df_empty.reindex(natsorted(df_empty.columns), axis=1)

  return df_empty  

def  Filenames_precandidates(_lista):
  # lista extend a partir de nested list python;
  vazio=[]
  c=1
  for f1 in _lista:
    if len(f1) != 0:
      for f in f1:
        nnbase = f.split('.')
        nbase=  nnbase[0] + '_'+str(c) + '.png'
        vazio.append(nbase)
    else:
      continue

    c+=1  
  
  return vazio  
   
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
    #print('nlabels:', nLabel)
    NLabels += nLabel

  QUARTILE = [int(np.percentile(Lista_areas_[i], percentile)) for i in range(nclasses)]                                                               
  return  QUARTILE 

def split_filenames_per_class(Listx,nclass):
  new_List = [[] for i in range(nclass)]  
  for fname in Listx:
    print('fname::>>', fname)
    c = fname.split('.')[0][-1]
    print('c1::>>', c)  
    #c = int(fname.split('.')[0][-1])
    new_List[int(c)-1] +=[fname]

  return new_List  
    
def gen_imgs_pd_i(pd_dict_i, Lista_i):
  """
  filtra  o pandas  só os index (filename )  de interesse:
  """  
  #Lindex = pd_dict_i.index.tolist()
  #new_ ==[itm  for itm in Lindex if itm not in Lista_except_i]  
  pdi = pd_dict_i[pd_dict_i.index.isin(Lista_i)]  
    
  return pdi   


def Ldir_plots(Lista_mk): #Lista_mask
  
  n0 = len(Lista_mk) # Lista_mi
  nList_ = [[] for i in range(n0)]
  for i in range(n0):  
    L01 = Lista_mk[i].split('.')[:-1]
    L1 = [item + '.png' for item in L01]
    nList_[i]=L1

  return nList_      

def filter_pd_(pd_, List_of_values):
  #df[df['A'] in list_of_values]
  new_pd_ = pd_[pd_['Lfilename'].isin(List_of_values)]   

  return new_pd_  

def nested_List_flatten(Lista_mk): # Lista_  = nested_List_flatten(Lista_mk)Lista_mk
  """
  Function to help to flatten a nested list.
  """
  List_Lk = Ldir_plots(Lista_mk)
  return [item for sublist in List_Lk for item in sublist]

        
def sum_pixelesX(List_1x, nclass, path_csv_info):
    # Separando imgs1x per classes:
    #print('dentro da funcao  sum_pixelesX:>')
    #
    #  List_1x >  flat list of files 1x 
  itemx = List_1x[0]  
     
  if itemx.count('_') >=3:
    split_Lfiles1  = split_filenames_per_class(List_1x,nclass)
    split_Lfiles = []  
                 
    for idy in range(nclass): 
      nlistax = split_Lfiles1[idy]
      listyz = nlistax[0]  
        
      list_z =[]
      for j in range(len(nlistax)):
        idz = nlistax[j].split('.')[0][:-2] + '.png'
        list_z.append(idz)  
        
      split_Lfiles.append(list_z)     
                   
      #print('Primer element  de split_Lfiles dentro do IF::', split_Lfiles[0][0])
       
  else:  
    
      #pass     
    split_Lfiles = List_1x 
        
    # Soma_Total:            
  df_info = pd.read_csv(path_csv_info)
  column_namesx = list(df_info.columns)
  Empty_ = split_Lfiles
    

  Sum_augm =[]             
  _c0 =0       
    
  for i in range(nclass): 
      column_namesx2 = column_namesx[2:]             
      sublist_i  = Empty_[i]    
      cols=['Filenames', 'c0',column_namesx2[i]] 
      new_dfx = df_info[cols]    
      Fh= new_dfx[new_dfx.Filenames.str.contains('|'.join(sublist_i))]
              
      Sumxi1 = Fh[Fh.columns[1:]].sum(axis=0)

      Sumxi = [int(item) for item in Sumxi1]
      a1,b = Sumxi      
      a= int(512*512*len(Fh.index)- b)   
      _c0 +=a          

      Sum_augm.append(b) 

  #print('pixeles de sum_augm:::>', Sum_augm)   
           
  Sum_ptotal_class = (np.array(Sum_augm)).tolist()

  Sum_ptotal= [_c0] + Sum_ptotal_class  


  return Sum_ptotal   


def pandas_sorted_by_columns(pd_):
    #pd_ = pd.read_csv(filepath_pd_in)
  cols_df = pd_.columns.tolist() 

  df_sorted_by_column= pd.DataFrame() 

  for j in range(len(pd_.columns)):
    col = cols_df[j]    
    L1 = pd_.loc[:,col].tolist()
    L11 = sample(L1, len(L1))  
    df_sorted_by_column[col]= L11   
    
        
  return df_sorted_by_column



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



def clean_hole(input_file, thresholdd):

  input_im = imread(input_file)

  img_pad = np.pad(input_im, ((2,2),(2,2)), 'maximum')

  new_img2 = img_pad

  markers = np.zeros_like(img_pad)
   
  markers[new_img2 < thresholdd] =1

  markers_sobel  = sobel(markers)

  new_im2 = ndi.binary_fill_holes(markers_sobel)

  new_image02 = new_im2[2:-2, 2:-2]

  input_im[new_image02] =0


  return input_im  
    

def make_img_bg(_mean_std_bg, img_size):
  
  sample = random.choice(_mean_std_bg)
  info_mean, info_std = sample[0], sample[1]
  randomnumber = round(random.normalvariate(info_mean, info_std))
  
  new_im = Image.new(mode='L', size=img_size)

  for x in range(img_size[0]):
    for y in range(img_size[1]):
      new_im.putpixel((x, y), randomnumber)

  return new_im




print('The end of UTILS_.PY')
       

 


