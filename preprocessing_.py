
from pathlib import Path, PureWindowsPath, PurePosixPath

import os
import platform 
from pathlib import Path, PureWindowsPath, PurePosixPath
from utils  import * 
from info_prm import *   
from process_pd2  import *    



  

def get_project_root_dir():
    print('XXXXXx')

    print(Path(__file__).absolute())
    print(Path(__file__).absolute().parent)
    return Path(__file__).absolute().parent.parent



def get_project_dir_dataset(dir_dataset):
    _path = str(Path.home())

    for root, dir, files in os.walk(_path):      
      for dirname in dir:       
        if dirname==dir_dataset:
          path_dir= os.path.join(root, dirname)
    return path_dir    
     

def preporcessing(IMG_dir):#, LABEL_dir):
    #check if format is correct in folder:#
    for filename in os.listdir(IMG_dir):
        print(filename)


    
def check_format_file(path3, ext_format):#, LABEL_dir):
    #check if format is correct in folder:#
    print(f"Checking format files in path {path3}")
    for filename in os.listdir(path3):
        #print("XXX":>>, path3 / filename)
        if not filename.endswith(ext_format):  
            print(f" Arquivo {filename} is have no format JPG")          
            os.remove(os.path.join(path3,filename))  

        else:
            pass
  
    print('checking...')
    return True  

     
_PATH = '/home/nbc/Documentos/Dataset_/'
    

def preproc():

    ######################
    
    print('[INFO]  Start preprocessing.....')
                  
    # create needed folders:
    make_folders(_PATH, FOLDERS)  
        
    #crea o primeiro csv pandas:>>'info_targets.csv'
    L_filenames = make_list_file(LABEL_dir) 

    
    csv_file = pclass_lista(L_filenames, 
                            LABEL_dir, nclass,  
                            saved_filename=TEMP1 +csv_file_nclass)

    binaries = binary_per_class_(LABEL_dir, 
                                DIR_MASK, 
                                L_filenames)
    
    # select candidates for build dataframe:
    Filenames_precandidates = make_list_file(DIR_MASK)

    # define n  quartil:
    nquartil= quartiles_x(Filenames_precandidates, 
                        DIR_MASK,  nclass, percentile)

    print(f'For  percentil value  {percentile}: List of percentile per class :{nquartil}')    

    pd_prefinal_analysis = pd_info_objects(Filenames_precandidates, 
                                        nquartil, 
                                        IMG_dir, DIR_MASK)


    # salvando o segundo frame:
    pd_prefinal_analysis.to_csv(TEMP1+  filename_pd_objects, index=False)

    return print(" preprocessing was sucessfully")






#a= preproc()

#print(a)
      
