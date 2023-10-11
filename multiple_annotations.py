
from utils import * 
from info_prm import * 

from mult_mask2 import *                
  
from dictionary_info import *
from multiple_imgs import *          
from process_pd2  import *
  
######################    
from ast import literal_eval  

random.seed(10)
    
####################### 

           
_PATH = '/home/nbc/Documentos/Dataset_/'

  
         
def  multiples_ann():

    listsx = LoadLists(nome_file_pkl)  
    Lnumber_imgs = listsx['Lnumber_imgs']    
    summm= sum(Lnumber_imgs)      
            
    M= max(Lnumber_imgs)  

    pd_fnames1 = making_pd_fn3(TEMP2, M, nclass)

    pd_fnames = pandas_sorted_by_columns(pd_fnames1)
        
    # get the start time  
    st = time.time()      

    # Lfn_to_removex ;  filenames 1x para ser deletado:::>
    Lfn_to_removex = WXZ(value_percent,pd_fnames, DATAx_2,LDIR_LABELS,
                        nclass, Lnumber_imgs)
                

    et = time.time()            
        
    # get the execution time
    elapsed_time = et - st    
    
    print('Execution time for masks  palette image 2x,3x,4x,5x,6x:', 
        elapsed_time, 'seconds')

    with open(nome_file_pkl, 'wb') as pickle_file:
        pickle.dump(Lfn_to_removex, pickle_file)#, protocol=pickle.HIGHEST_PROTOCOL)
            

    return print('Mulriplas annotations were done sucessfully')                  
    
#a5 = multiples_ann()
#print(a5)
