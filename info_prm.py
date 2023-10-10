
_PATH = '/home/nbc/Documentos/Dataset_/'   

#Parameters:
size_image =(512,512)  
Threshold0 = 0.008 # 0.2%
    
nclass = 6    
      
VALOR = 900000           
percentile = 30          
percentile_max = 80         

value_percent= 0.99 #  80%       
                
# Given a threshold:       
X=  500                                                                                         
                        
                                              
Lsamples_min=[6, 6, 6, 10, 4, 8]  
Lsamples_max =[10, 25, 10, 55, 10, 30]    
    
ext_jpg = 'jpg'    
ext_png = 'png'
str_ ='_0'         
        
      
#####            
###  =====  Step 1:
#####  create  folders  into path:
# folders necessários:

subfolder = ['imgs_/', 'labels_/']    

LISTA_CLASSES = [ 'class/class{}/{}'.format(str(i), str(str_)) for i in range(1,nclass+1) for str_ in subfolder]
Datax_ = ['Dataset_imgs_labels/' + item for item in subfolder]
temp_ = [ 'temp/info/', 'temp/info_csv/']
mask_ = ['binary_masks/']  
FOLDERS = LISTA_CLASSES + Datax_ + temp_ + mask_ 

#  Create  folders in root:
#outx = make_folders(_PATH, FOLDERS)
       
# Redefine folders:   
IMG_dir = _PATH + 'imgs_/'    
LABEL_dir = _PATH + 'labels_/'
DIR_MASK = _PATH + mask_[0]
    
DATAx_1 = _PATH + Datax_[0]  
DATAx_2 = _PATH + Datax_[1]
  

TEMP1 = _PATH + temp_[0] # info
TEMP2 = _PATH + temp_[1] #temp/info_csv

LDIR_IMGS = [_PATH + LISTA_CLASSES[2*i]   for i in range(nclass)]

LDIR_LABELS  = [_PATH + LISTA_CLASSES[2*i +1]   for i in range(nclass)]

# images =[img for img in os.listdir(image_path) if img.endswith(".jpg")]  
    
nome_file_pkl =  TEMP1 + 'info_result_0.pkl'  

    
a1 = 7

Lista_mean_bg = [57.916259765625 - a1, 53.35888671875 -a1, 44.46533203125 -a1]
Lista_std_bg = [3.10549683948025, 2.2441567203751296, 2.8419069039454388]

mean_std_tuple = list(zip(Lista_mean_bg, Lista_std_bg))

filename_pd_objects = 'pd_info_objects_final.csv'  

csv_file_nclass = 'info_targets.csv'

  