#import pickle 
from info_prm import *

from utils import * 

#from gen_mask import *   
#from multiple_masks import *   
#from dictionary_info import *
#from multiple_imgs import *
#from process_pd2  import *
#from single_img import *  
         
##  Listas_filtradas: Lista_total - Lista_to_remove     
##  Criando  images masks  sobre listas filtradas:
## From LDIR_IMGS/LDIR_LABELS to DATAx_2 (para teste - trocar por multiclass_imgs/)

######################
        

_PATH = '/home/nbc10/Documentos/Dataset_/'



  
#  newL = [item for item in lista1 if item not in lista2]

#from ast import literal_eval

#pd_final_info2 = pd.read_csv(TEMP1 +  'pd_info_objects_final.csv',
#                 converters={'intensity_image': literal_eval,
#                             'Nclass': literal_eval},
#                 usecols = ['Nclass', 'intensity_image'] ) 
  

def completing_imgs():

  open_file = open(nome_file_pkl, "rb")
  loaded_list = pickle.load(open_file)

  open_file.close()  
    
  List_1x  = loaded_list       

  # Separando imgs1x per classes:
  Lista_split02 = split_filenames_per_class(List_1x,nclass)

  missL_class =[ []*i for i in range(nclass)]

  for i in range(nclass):
    set1 = set(make_list_file(LDIR_LABELS[i]))
    #print('len de set1:>>', len(set1))

    set2 = set(Lista_split02[i])
    #print('len de set2:>>>', len(set2))

    #missL[i] =[item for item in Lfilename_total[i] if item not in Lista_split02[i] ]
    missL_class[i] = list(set1.difference(set2))
    #print('len de missL1_i que falta per classes:>>>', len(missL_class[i]))


  with open(TEMP1 + 'Lmissing_1x_per_class.pkl', 'wb') as pickle_file:
      pickle.dump(missL_class, pickle_file)#, protocol=pickle.HIGHEST_PROTOCOL)
                
  out_path_jpg= DATAx_1 #/Dataset_imgs_labels/imgs_/
  out_path_png = DATAx_2 

  #print('Finalizando  a copia dos arquivos  de imgs grayscale:')
  for i  in range(nclass):
    Lij = missL_class[i]
    for item in Lij:     

      shutil.copy(LDIR_LABELS[i] + item, out_path_png) 
      #print('PNG files  faltantes  copiados...')           

      novo_item = item.replace('mask', 'imgs').replace('png', 'jpg')
      #print('novo item>::', novo_item)
      x = novo_item.split('.')[0]
      #print('x:', x)
      y = int(x[-1])-1  
      #print('in_dir', LDIR_IMGS[y] + novo_item)
      #print('out_dir', out_path_jpg)
    
      shutil.copy(LDIR_IMGS[y] + novo_item, out_path_jpg)  
      #print('JPG files  faltantes  copiados...')


  return print('JPG and files  faltantes  foram  copiados...')        
            
        
        
#print('Main_part6 script is done... ')
          
    
        


            