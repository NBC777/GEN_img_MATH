#import pickle 
from info_prm import *

from utils import * 

######################
        

_PATH = '/home/nbc/Documentos/Dataset_/'

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

    set2 = set(Lista_split02[i])

    #missL[i] =[item for item in Lfilename_total[i] if item not in Lista_split02[i] ]
    missL_class[i] = list(set1.difference(set2))
 

  with open(TEMP1 + 'Lmissing_1x_per_class.pkl', 'wb') as pickle_file:
      pickle.dump(missL_class, pickle_file)#, protocol=pickle.HIGHEST_PROTOCOL)
                
  out_path_jpg= DATAx_1 #/Dataset_imgs_labels/imgs_/
  out_path_png = DATAx_2 

 
  for i  in range(nclass):
    Lij = missL_class[i]
    for item in Lij:     

      shutil.copy(LDIR_LABELS[i] + item, out_path_png)          

      novo_item = item.replace('mask', 'imgs').replace('png', 'jpg')
      x = novo_item.split('.')[0]
  
      y = int(x[-1])-1  
    
      shutil.copy(LDIR_IMGS[y] + novo_item, out_path_jpg)  
  
    
  files_imgs = sorted(make_list_file(DATAx_1))
  files_labels= sorted(make_list_file(DATAx_2))

  if len(files_imgs) ==len(files_labels):
    try:
      list_filenames = zip(files_imgs, files_labels)
      i=0   
      for item in list(list_filenames):
        f1, f2 = item

        old_filepath_f1 = os.path.join(DATAx_1, f1)
        new_name_f1 = 'imgs_' + str(i) + '.' + ext_jpg
        new_filepath_f1 = os.path.join(DATAx_1, new_name_f1)

        old_filepath_f2 = os.path.join(DATAx_2, f2)
        new_name_f2 = 'mask_' + str(i) + '.' + ext_png
        new_filepath_f2 = os.path.join(DATAx_2, new_name_f2)

        os.rename(old_filepath_f1, new_filepath_f1)
        os.rename(old_filepath_f2, new_filepath_f2)
        i+=1

    except FileExistsError:
      print('File not matched.')   

  return print('JPG and files  faltantes  foram  copiados...')        
            


#a10 = completing_imgs()

#print(a10)
     


            
