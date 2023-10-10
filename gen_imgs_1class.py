
from utils  import * 
from info_prm import * 

from single_img import *  

          
                               
######################  
 
from ast import literal_eval  

  
#######################
#  Nesse folder vamos gerar  images  desde a mascara para cada um das classes:
#########################  

# read specific columns of csv file using Pandas

_PATH = '/home/nbc/Documentos/Dataset_/'
    
from ast import literal_eval



##
##
#
  
print('=============')


#print('ARQUIVO GERA IMGS 1X ::>> ')
def gen_imgs_one_class():


  pd_final_info2 = pd.read_csv(TEMP1 +  filename_pd_objects,
                 converters={'intensity_image': literal_eval,
                             'Nclass': literal_eval},
                 usecols = ['Nclass', 'intensity_image'] ) 
    

  # get the start time     
  st = time.time()   
    
  Lfilename_total =[]  
  for i in range(nclass):
    Lfilename_total.append(make_list_file(LDIR_LABELS[i]))
        

  #print('len de filename', len(Lfilename_total))    
          

  pd_ =  pd_final_info2.copy()          
      
  outx = GEN_IMGS_one_class(nclass, pd_, mean_std_tuple,
                            LDIR_IMGS, LDIR_LABELS,
                            Lfilename_total, TEMP2)

        
                    
  # get the end time
  et = time.time()         
                
  # get the execution time
  elapsed_time = et - st
  return print(f'Execution time for generate ALL GRAYSCALE image: {elapsed_time}  seconds')


