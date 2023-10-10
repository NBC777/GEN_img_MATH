from utils  import * 
from info_prm import * 
   
from process_pd2  import *    

    
 #    Outliers in the data may causes problems during model fitting (esp. linear models).
#    Outliers may inflate the error metrics which give higher 
# weights 
#to large errors (example, mean squared error, RMSE). 
              
######################
    
  
#######################


     
print(' Start  main 1.....')
           
_PATH = '/home/nbc10/Documentos/Dataset_/'
  
#  1:      
# create needed folders:
make_folders(_PATH, FOLDERS)  
    
#check_file_bg = os.path.isfile(_PATH + 'background.jpg')
     
    
#crea o primeiro csv pandas:>>'info_targets.csv'
L_filenames = make_list_file(LABEL_dir) 

  
csv_file = pclass_lista(L_filenames, 
                        LABEL_dir, nclass,  
                        saved_filename=TEMP1 +'info_targets.csv')
#le o csv para extrair dados:
pd.read_csv(TEMP1+ csv_file_nclass)  

# binary_per_class_(in_path, path_save, Lista_targets)
   #in_path, path_save, Lista_targets, nclass   
#binarizar aqueles que já foram sinalizadas:
binaries = binary_per_class_(LABEL_dir, 
                            DIR_MASK, 
                            L_filenames)
 

print('All files was created .....')         

 
# select candidates for build dataframe:
Filenames_precandidates = make_list_file(DIR_MASK)

#print('len de Lista_precandidatos1:', len(Filenames_precandidates))

# define n  quartil:
nquartil= quartiles_x(Filenames_precandidates, 
                      DIR_MASK,  nclass, percentile)

print(f'Percentile_min per class :{nquartil}')    

pd_prefinal_analysis = pd_info_objects(Filenames_precandidates, 
                                       nquartil, #nquartil2, 
                                       IMG_dir, DIR_MASK)

#print('Len de pd_final_analysis', len(pd_prefinal_analysis))

#print('columns de pd:>', list(pd_prefinal_analysis.columns))

# salvando o segundo frame:
pd_prefinal_analysis.to_csv(TEMP1+  filename_pd_objects, index=False)

# 5518  objetos  gerados: 
print(" preprocessing was sucessfully")


            
            