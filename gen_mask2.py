from utils import *
from collections import Counter 
from info_prm import *

import cv2
  


def allocation_quadrant(theta, dict_quadrants, bbox_, h,w):

  a, b, c, d = bbox_

  if a==0 and b==0:
    num_quadrant = 0

  elif b==0 and c ==h:
    num_quadrant =1

  elif c ==h and d ==w:
    num_quadrant=2

  elif a==0 and d==w:

    num_quadrant =3   
    
  #print('Num_quadrante:>>>', num_quadrant)


  if theta==90:
    s =1

  elif theta ==180:
    s =2

  elif theta==270:
    s=3

  new_quadrant = (num_quadrant + s)%4

  x, y, x_final , y_final = dict_quadrants[new_quadrant]

  return x, y, x_final, y_final  


def search_new_xy_boder(w,h,w0,h0, t, Trs1, a,b,c,d, corner=True):  

  if corner:
    Trs = 10000
    
  else:
    Trs = Trs1        

  if t==0: 


    if h-h0 < Trs or corner:

      x=0
      y=0

    else:

      
      if b==0:
        y =w - w0

      elif d ==w:
        y = 0

      x = random.randrange(h-h0)

  else:

    if w-w0 < Trs or corner:

      x=0
      y=0

    else:

      if a==0:
        x = h - h0  

      elif  c==h:
        x =0

      y = random.randrange(w-w0) 

  x_final = x + h0
  y_final = y + w0

  return x, y, x_final, y_final


def  rdm_coord_angle(patch_res, bbox_,h, w, mode_type=None):
  #mode_type  correspond to a mode before  rotation of patchs
  patch_empty = np.empty(patch_res.shape, dtype=int)
  if mode_type =="inner":    
   
    theta = random.randrange(360)
    patch_res_rot = ndimage.rotate(patch_res, theta)     
    p_h, p_w = patch_res_rot.shape

    if (p_h < h) and (p_w < w):  

      x = random.randrange(h- p_h)  
      y=random.randrange(w - p_w)
  
      x_final = x+ p_h
  
      y_final = y+ p_w   

      patch_empty = patch_res_rot       



    else:
        h3 = min(p_h,h)
        w3 = min(p_w,w)  

        x = 0
        y=0
        x_final = x+ h3
        y_final = y+ w3

        patch_empty = patch_res_rot[:h3,:w3]     

  else:
   
    a, b, c, d = bbox_ 
    count_bbox = Counter(list(bbox_))
    num_intersection_ = count_bbox[0] + count_bbox[512]
    
    Trs1 = 10 
    a, b, c, d = bbox_

    if num_intersection_ ==1:

      theta = 180

      #a, b, c, d = bbox_
      if b ==0 or d ==w:
        t=0
      elif a==0 or c==h:
        t=1           

      patch_res_rot = ndimage.rotate(patch_res, theta)    

      h0, w0 = patch_res.shape

      h0 = min(h,h0)  
      w0 = min(w,w0)   
      # search_new_xy_boder(theta,w,h,w0,h0, Trs1, corner) 
      x, y, x_final, y_final = search_new_xy_boder(w,h,w0,h0, t, Trs1, a,b,c,d, corner=False)

    else:

      theta_list = [90,180,270]
      theta = random.choice(theta_list)
      patch_res_rot = ndimage.rotate(patch_res, theta)
      h0, w0 = patch_res_rot.shape

      h0 = min(h,h0)
      w0 = min(w,w0)    

      dict_coords = [(0,0,h0,w0), (h-h0,0,h,w0), (h-h0,w-w0,h,w), (0,w-w0,h0,w)]

      x, y, x_final, y_final = allocation_quadrant(theta, dict_coords, bbox_, h,w)

    patch_empty = patch_res_rot[:h0,:w0]  

 
  return theta, x,y, x_final, y_final, patch_empty   


def  sorted_index_per_area(pd_patch,index_random_):
    pd_areas = pd_patch.loc[index_random_,['area']] 
    sorted_pd_areas = pd_areas.squeeze().sort_values(ascending=False)
    return  sorted_pd_areas.index.tolist()
    
         
def transform_patch_i(p_i,min_scale, max_scale, bbox_, h,w, mode_type="inner"):

    scale = round(random.uniform(min_scale, max_scale),3)
    patch_h, patch_w = p_i.shape  
    resize_patch = cv2.resize(p_i,(int(patch_w * scale),int(patch_h * scale)))

    if mode_type=="inner":
        theta, x,y, x_final, y_final, patch_empty = rdm_coord_angle(resize_patch, bbox_,h, w, mode_type="inner")

    else:
        
        theta, x,y, x_final, y_final, patch_empty = rdm_coord_angle(resize_patch, bbox_,h, w, mode_type="border")

    return theta, scale, x, y, x_final, y_final, patch_empty 

   
def sub_patchs(pd_i, list_idx, max_tentativas):
    img = np.zeros((512, 512), dtype="uint8")
   
    h, w = img.shape      
    min_scale = 0.95   
    max_scale = 1.15  
    Lista_theta=[]  
    Lista_resize =[]  
    Lista_object = []
    Lista_fnames = [] 
    Lista_x = []
    Lista_y = []
    
    Lista_excep_index =[]  
   
    for i in list_idx:

      patch_ = pd_i['mask_image'][i]  
      patch_obj = int(pd_i['label'][i])   
      patch_fnames1 = pd_i['Filename'][i] 
      bbox_ = pd_i['bbox'][i]
      fname2 = patch_fnames1.split('.')[0][6:]  
    
      patch = np.array(patch_).astype('uint8')

      mode_type = pd_i['Type'][i]

      z=0
      # z : num_tentativas
      scale=0
      theta =0
      x =0
      y =0
 
      patch_empty = np.empty(patch.shape, dtype=int) 

      no_bool= True
    
      max_tentativa = 15   
    
      while no_bool and  z < max_tentativa:   
        
        dict_info  = transform_patch_i(patch, min_scale, max_scale, bbox_, h,w, mode_type=mode_type)
        theta1, scale1, x1,y1, x_final1, y_final1, patch_empty= dict_info 

        seg1 = img[x1: x_final1, y1:y_final1]  
  
        _bool =   (cv2.bitwise_and(seg1, patch_empty)==0).all()
        
        no_bool = not _bool     

        theta, scale, x, y, x_final,y_final =theta1, scale1, x1, y1, x_final1, y_final1
        p = patch_empty     
        seg = seg1

        z+=1    
          
      #print(scale, theta, x, y, x_final,y_final)


      seg[:] = cv2.bitwise_xor(seg, p)
  
      Lista_excep_index.append(i)

      Lista_x.append(x)             
      Lista_y.append(y)            
      Lista_fnames.append(fname2)
      Lista_object.append(patch_obj)
      Lista_resize.append(scale)         
      Lista_theta.append(theta)

    return img, Lista_fnames, Lista_object, Lista_theta, Lista_resize, Lista_x, Lista_y  



def  generate_masks_n(pd_patch, dir_to_save, SUM_TOTAL, samples_min, samples_max, n): 

  LTHETA=[]  
  LRESIZE=[]  
  LINDEX=[]
  LOBJECT = []  
  LFNAMES = []     
  
  L_x=[]  
  L_y=[]        
  L_o =[]
  min_scale = 0.9     
  max_scale = 1.1   
  Lfilename =[]

  sum = 0         
  i=0             
                   
  while sum < SUM_TOTAL:
    #print('I:>>>>>>>>>>>>>>>>>>>>>>>',i)
    #background = Image.open(_PATH + 'background.jpg') 
    rnd = random.randint(samples_min, samples_max) 
    index= pd_patch.index.tolist()
    index_random_= random.sample(index, rnd)

    index_random = sorted_index_per_area(pd_patch,index_random_)   

    max_tentativas = 10
    mask_array,Lista_fnames,Lista_object,Lista_theta,Lista_resize,Lista_x,Lista_y =sub_patchs(pd_patch, index_random, max_tentativas) 
    
    non_zeros = np.count_nonzero(mask_array)    
    sum += non_zeros

    im123= Image.fromarray((mask_array * n).astype('uint8'))#, mode='P')  
    im123.putpalette(palette_from_dict(colors_dict))

    file_ = 'label_{}_{}'.format(i,n)
    
    im123.save(dir_to_save + file_ + '.png', "PNG")
    
    LTHETA.append(Lista_theta)
    LRESIZE.append(Lista_resize)
    L_x.append(Lista_x)    
    L_y.append(Lista_y)
    LINDEX.append(index_random)  
    LFNAMES.append(Lista_fnames)
    LOBJECT.append(Lista_object)    
    Lfilename.append(file_ + '.png') 
     
    i+=1      
    
      
  Xdictionary= { 'Lfilename':Lfilename, 'Lfnames':LFNAMES, 'Lobjects':LOBJECT,
                 'LTheta': LTHETA, 'LRESIZE': LRESIZE,
                'LINDEX': LINDEX, 'L_x': L_x, 'L_y':L_y}
                    
  return sum, Xdictionary,i    
    


def generate_ALL_masks(pd_, SUM_px, nclass, temp_dir,
                                Ldir_target, Lsamples_min, 
                                Lsamples_max, show_pd = False):

  Lista_sum = [0 for i in range(nclass)]  
  Lnumber_imgs =[0 for i in range(nclass)]
  columns_ = ['Lfilename', 'LTheta', 'LRESIZE', 'LINDEX', 'L_x', 'L_y']
  pd_empty = pd.DataFrame(columns = columns_)

  for i in range(nclass):      
    n=i+1  
  
    SUM_TOTAL_i = SUM_px[i] 
    dir_out= Ldir_target[i]            
    samples_min = Lsamples_min[i]        
    samples_max=Lsamples_max[i]

    pd_n = pd_[pd_['Nclass']== n]  

    st1 = time.time() 
    sum, dictionary, num_img = generate_masks_n(pd_n, dir_out, SUM_TOTAL_i, 
                                           samples_min, samples_max, n)
    end = time.time()  
    print("Time to generate imgs of class %d:  %s seconds ---" % (i+1, end - st1))
    Lista_sum[i] =sum 
    Lnumber_imgs[i] = num_img        
    pd_dict = pd.DataFrame(dictionary)          
    if show_pd:
      pd_empty = pd.concat([pd_empty, pd_dict], axis=0)
    else: 
      path = os.path.join(temp_dir,'info_csv')  #  arreglar  aqui:: 
      os.makedirs(path, exist_ok = True)
      pd_dict.to_csv(temp_dir  + 'selection_objects_class_{}.csv'.format(i+1), index=False)
      #print(f"save file: selection_objects_class_{i+1}.csv")
          
      pd_empty = None  
      
  #print('Total execution time:', time.time() - st0, 'seconds')  
  print('All mask images  were generated successfully...')  
       
  return   Lista_sum, Lnumber_imgs, pd_empty 

