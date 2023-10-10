#from libraries import *
from utils import *
from info_prm import * 


  

#####################
from ast import literal_eval  
########################
# vamos criar um novo dictionary com dados dos csvs:

_PATH = '/home/nbc10/Documentos/Dataset_/'
    
from ast import literal_eval

""" 

pd_final_info3 = pd.read_csv(TEMP1 +  'pd_info_objects_final.csv',
                 #converters={'Filename': literal_eval,    
                   #'intensity_image': literal_eval,
                   #          'Nclass': literal_eval,    
                 #            'area': literal_eval},  
                 usecols = ['Filename',  'area'] ) 

pd_final_info2 = pd.read_csv(TEMP1 +  'pd_info_objects_final.csv',
                 converters={'intensity_image': literal_eval,
                             'Nclass': literal_eval},
                 usecols = ['Nclass', 'intensity_image'] ) 


"""  


def new_dict_pd(dir_csv, Lista_):
  Lista_csv = make_list_file(dir_csv)
  n1 = len(Lista_csv)
  pd_vazio=pd.DataFrame()

  for k in range(n1):
    #print('K:::',  k)
    fnamex = Lista_csv[k]
    c0 = fnamex.split('.')[0]       
    c=int(c0[-1])            
    L_target = Lista_[c-1]    
    pd_dict_i = pd.read_csv(dir_csv + fnamex,
                            converters={'Lfnames':literal_eval,
                                        'Lobjects':literal_eval,
                                        'LTheta':literal_eval,
                                         'LRESIZE': literal_eval,
                                         'LINDEX': literal_eval,
                                        'L_x':literal_eval,
                                        'L_y':literal_eval})

    if len(pd_dict_i) !=0:
      new_pd = filter_pd_(pd_dict_i, L_target)  

      pd_vazio = pd.concat([pd_vazio,new_pd], axis=0)
    else:

      pass 

  pd_vazio = pd_vazio.reset_index()

  if 'index'  in pd_vazio.columns:
    del pd_vazio['index']

  else:  
    pass
   
  return pd_vazio


    