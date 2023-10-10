from utils import *
from info_prm import *

_PATH = '/home/nbc/Documentos/Dataset_/'

import cv2
 
def img_matrix4(pd_filter_Lk, pd_i):#, Lm_k, background): 
  #print('====   DENTRO  DO  IMG_MATRIX4  === ')
  Lindex = pd_filter_Lk.index.tolist() 
  M0 = len(Lindex)

  size_image = (512,512)      
  zeros = np.zeros(size_image, dtype='uint8') 
  
  for ix in Lindex:

    row = pd_filter_Lk.loc[ix].tolist()     

    M1 = len(row[4])  

    i = 0
    while   i < M1: 
   
        patchx_k = pd_i[row[5][i]] # acabei de mudar de 4 para 5:
        #print('pd_i[row[4][i]]:', row[5][i])
        #print('patchxk_:', patchx_k)   
      
        patch = np.array(patchx_k).astype('uint8')    
        patch_h, patch_w = patch.shape
        scale = row[4][i]      
        theta = row[3][i]  

        p = ndimage.rotate(cv2.resize(patch,(int(patch_w * scale),int(patch_h * scale))), theta)
        p_h, p_w = p.shape
        x = row[6][i]              
      
        y = row[7][i]      
        zeros[x: x + p_h, y: y + p_w] = p 
        i+=1     

  return zeros   

def BUILD_X4(_PATH, dir_csv, dirx , pd_intensity, pd_dict, 
             dir_out, dir_i,s=3):
  """ 
  dirx: folder where a multiple mask is.   
  dir_out : folder dirx
  dir_i : folder to save imga JPG images.
     
  """  
   
  List_mi = make_list_file(dirx)       
  List_mask = Ldir_plots(List_mi)               
              
  M = len(List_mi) 
              
  size_image = (512,512)  

  zeros = np.zeros(size_image, dtype='uint8')     
  k=0 
          
  while k < M: 

    Lk = List_mask[k]   

    N0 = len(Lk)         
    
    pd_filter_Lk = filter_pd_(pd_dict, Lk)  

    zerosx  =img_matrix4(pd_filter_Lk, pd_intensity)  
      
    imgg = Image.fromarray(zerosx.astype('uint8'), mode='L') 
    Ffilex = List_mi[k] 

    a = Ffilex.split('.')[:-1]  
    ref_lista= [int(item[-1]) for item in a ]
   
    mask_1 = imgg
    mask_2 = Image.open(dir_out + Ffilex).convert('L')#, "PNG")
   
    background = make_img_bg(mean_std_tuple, size_image)
    background.paste(imgg, (0,0), mask=mask_1)
    background.paste(imgg, (0,0), mask=mask_2)             
         
    if k % 2 ==0:    

      factor = round(random.uniform(0.8,1),2)          
      image_modify = ImageEnhance.Contrast(background)
      imgz=image_modify.enhance(factor)
    else:
      #brightness:         

      factor = round(random.uniform(1,1.4),2)

      image_modify = ImageEnhance.Brightness(background)
      imgz= image_modify.enhance(factor)
  
    #try:      

    arr= np.asarray(imgz).astype('uint8')  
    im=Image.fromarray(arr, mode='L')  
    
    ffile_jpg = Ffilex.replace('mask','imgs').replace('png', 'jpg')
    im.save(dir_i + ffile_jpg, "JPEG")
              
    k +=1                           
            
  print(' All images of class {} were generated sucessfully ...')
  return True   
  


  