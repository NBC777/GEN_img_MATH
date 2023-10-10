#import pickle 
from info_prm import *
from utils import * 
#from gen_mask import * 
#from multiple_masks import *   
from dictionary_info import *
from multiple_imgs import *
#from process_pd2  import * 

# criar images mode L de maskaras muktiples:
    
   
######################    

_PATH = '/home/nbc/Documentos/Dataset_/'

##############################
#import cv2  
#import time   
from ast import literal_eval  
from timeit import default_timer as timer 
#import os      

# Cria  images das mascaras multiples
#  Mascaras de Datax_2  para folder images DATAx_1
#      
          
#############################


# extract  list  flatten to remove:
#with open('filename_to_remove.pkl', 'rb') as pickle_load:
#    lista_to_remove_flatten = pickle.load(pickle_load)
    
from ast import literal_eval


    

#with open('filename_to_remove.pkl', 'rb') as f:
#    Lfn_except_flatten = pickle.load(f)

def gen_images_nclasses():


      pd_final_info2 = pd.read_csv(TEMP1 +  'pd_info_objects_final.csv',
                 converters={'intensity_image': literal_eval,
                             'Nclass': literal_eval},
                 usecols = ['Nclass', 'intensity_image'] ) 

      # get the start time  
      st = time.time()  

      # Lista extendida dos filenames de multiples classes:
      Lista_ = make_list_file(DATAx_2)
      Lista_except_flatten = nested_List_flatten(Lista_)     
      Lista_split01 = split_filenames_per_class(Lista_except_flatten, nclass) 


      new_dict  = new_dict_pd(TEMP2, Lista_split01)                
                              
      pd_dict = new_dict.copy()     
      ##### 
      pd_intensity = pd_final_info2['intensity_image']
      
      dir_i = DATAx_1  
      dirx = DATAx_2   
      dir_out = dirx        

      out4_ = BUILD_X4(_PATH, TEMP2, dirx , pd_intensity, pd_dict, 
                  dir_out, dir_i,s=3)

      # get the end time  
      et = time.time()            
            
      # get the execution time
      elapsed_time = et - st      

      print('Execution time for generate grayscale image  from mask2x3x4x5x6x::', 
            elapsed_time, 'seconds')
      return print("All the n classes imagens  were created ")
#print(' Main_part5 script  done...')    
              