from utils import * 
from info_prm import *  
  
from gen_mask2 import *
                     
         
######################
import cv2  
import time   
from ast import literal_eval       
from timeit import default_timer as timer 
  
  
#######################


        
_PATH = '/home/nbc/Documentos/Dataset_/'
    
        

  
def  gen_all_masks():

      pd_final_info2 = pd.read_csv(TEMP1 +  'pd_info_objects_final.csv', 
                             converters={'label':literal_eval,
                                         'intensity_image': literal_eval,
                                         'bbox':literal_eval,
                                         'mask_image': literal_eval})#, index=False)


      st = time.time()     
    
      valor_list = [VALOR]*nclass

      data ={} 
      #nome_file_pkl =  TEMP1 + 'info_result_methods.pkl'
      SaveLists(data, nome_file_pkl)

      Lista_result = LoadLists(nome_file_pkl)

      Lista_result['Total_values']= valor_list   
      write_list(Lista_result, nome_file_pkl)       
      

      #print('Vamos gerar todas as mascaras em folder  class1/labels, class2/labels, ...')

      Lista_sum, Lnumber_imgs, pd_empty  =generate_ALL_masks(pd_final_info2, 
                                                            valor_list,
                                                            nclass, TEMP2,
                                                            LDIR_LABELS, 
                                                            Lsamples_min, 
                                                            Lsamples_max, 
                                                            show_pd = False)
      
      # get the end time
      et = time.time()                  
            
      # get the execution time  
      elapsed_time = et - st    

      print('Execution time for generate ALL mask palette image:', 
            elapsed_time, 'seconds')


      print('Number of images, per class,  generated:', Lnumber_imgs)
      print('Sum of pixels, per class, in generated images:', Lista_sum)      


      Lista_result['Lnumber_imgs']=Lnumber_imgs
      write_list(Lista_result, nome_file_pkl)

      Lista_result['Lista_sum']=Lista_sum
      write_list(Lista_result, nome_file_pkl)

      return print('[INFO] All labeled images were generated:')
    
#a2 = gen_all_masks()
#print(a2)
  



     
 



