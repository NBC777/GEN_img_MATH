from utils  import *
import cv2  
from PIL import ImageEnhance   
from ast import literal_eval
#=============================

_PATH = '/home/nbc/Documentos/Dataset_/'
         
    
def  generate_imgsZ(pd_dict, mean_std_tuple, pd_i,dir_i, dir_out, M, n):
  #print('3:  generate  imges FUNCTION ')  
  """
  pd_dict : pandas from dictionary with Lfinelanmes as index
  INT_i  Intensity values series  
  j :  number of image
  k : number of object in each j 
  """  
           
  for j in range(M):# j < M:    
      
    size_image = (512,512)   
    h,w = size_image     
    zeros = np.zeros(size_image, dtype='uint8')  

    background = make_img_bg(mean_std_tuple, size_image)

    row = pd_dict.iloc[j].tolist() 

    for k in range(len(row[4])): 

      patchx_k = pd_i['intensity_image'][row[4][k]]
      patch = np.array(patchx_k).astype('uint8')   
      patch_h, patch_w = patch.shape
       
      scale = row[3][k]  
      theta = row[2][k]             

      p = ndimage.rotate(cv2.resize(patch,(int(patch_w * scale),int(patch_h * scale))), theta)
      p_h, p_w = p.shape
   
      p_h= min(h, p_h)
      p_w = min(w,p_w)

      p = p[:p_h, :p_w]
   
      x = row[5][k]          
      y = row[6][k]  

      zeros[x: x+ p_h, y:y+p_w] = p       
    imgg = Image.fromarray(zeros, mode='L') 

    ffile_ =pd_dict.index.tolist()[j]  

    #if n==3:
    mask_ = Image.open(dir_out + ffile_).convert('L')#, "PNG")
    #else:
    #  mask_ = imgg    

    background.paste(imgg, (0,0), mask=mask_)           

    factor = round(random.uniform(0.9,1.1),2)

    if j % 2 ==0:  

      # contrast
      image_modify = ImageEnhance.Contrast(background)
      imgz=image_modify.enhance(factor)      
    else:
      #brightness:  
      # 
      #    
      image_modify = ImageEnhance.Brightness(background)
      imgz= image_modify.enhance(factor)

    try: 

      im = imgz              
     
      ffile_jpg = ffile_.replace('mask','imgs').replace('png', 'jpg')
      im.save(dir_i + ffile_jpg, "JPEG")
    except AttributeError:
      print("Couldn't save image {}".format(im))
            
    #j +=1    
      
  print(' All images   were generated sucessfully')

  return True    
    
        
    
def  GEN_IMGS_one_class(nclass, pd_, mean_std_tuple,
                         Ldir_in, Ldir_out, Lista_, dir_csv):
  """
  Ldir_in :  folder to save
  Ldir_out:  folder where is the label images
  Lista_:  List to be filtered filenames
  dir_csv:  temp/info_csv/    
  """
  
  Lista_csv = make_list_file(dir_csv)
     
  for i in range(nclass): 
    
    fname_ = Lista_csv[i]  
    n = int(fname_.split('.')[0][-1])  
  
    pd_dict_i = pd.read_csv(dir_csv + fname_,
                            converters={'LTheta':literal_eval,
                                         'LRESIZE': literal_eval,
                                         'LINDEX': literal_eval,
                                        'L_x':literal_eval,
                                        'L_y':literal_eval})
    pd_dict_i.set_index('Lfilename', inplace=True)
    Lista_except_i= Lista_[n-1]   
    pd_dict = gen_imgs_pd_i(pd_dict_i, Lista_except_i)
    #print('lista_index:::>>',  pd_dict.index.tolist())
    M = len(pd_dict.index.tolist())

    #print('value of M>>>', M)
        
    if  M >0: 
      pd_i = pd_[pd_['Nclass']==n] 

      dir_i = Ldir_in[n-1]  
      
      dir_out = Ldir_out[n-1]      
      out_ = generate_imgsZ(pd_dict, mean_std_tuple, pd_i, dir_i, dir_out, M, n)

    else:                  
                                   
      pass
  
  print(' All images  were generated sucessfully ...')  
  return out_      


    
    




    
    
