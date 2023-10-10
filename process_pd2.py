#from libraries import *
from utils import * 
from info_prm import *  
    

        
  
def pd_info_features(fname_, dir_binary, dir_img, 
                     Lista_quartile, 
                     #Lista_quartile_max
                     ):
            
  base = (fname_.split('.')[0]).split('_')  
  nbase = base[1] + "_" + base[2] + ".jpg"

  c = int(base[3])     
  img_ =  imread(dir_img + nbase)  
  img_binary =  imread(dir_binary + fname_)    
  labels = label(img_binary) 
  phases_= regionprops(labels, img_)  

  quartile =Lista_quartile[c-1]  
  #quartile_max = Lista_quartile_max[c-1]

  Lista_file =[]
  Lista_nclass=[]
  Lista_label=[]
  Lista_bbox=[]
  Lista_type =[]
   
  Lista_intensity=[]  
  Lista_area =[]
  Lista_mask = []    

  for region in phases_:
    
    cond1= (region.area > quartile)# and (region.area < quartile_max) 
    cond2= (512  in region.bbox) or (0  in region.bbox)
          
    if cond1:     
      Lista_file.append(fname_)  
      Lista_nclass.append(c)
      Lista_label.append(int(region.label))  
      Lista_bbox.append((region.bbox))
      

      #Lista_centroid.append(tuple(region.centroid))
      #Lista_coords.append(np.array(region.coords).tolist())
      Lista_intensity.append(np.array(region.intensity_image).tolist())               
      Lista_area.append(region.area)  
      Lista_mask.append((np.array(region.image)*1).tolist())

      if cond2:
        Lista_type.append("border")
      else:
        Lista_type.append("inner")
    
    else:
      continue  

  # Create the dataframe
  df4 = pd.DataFrame({'Filename':Lista_file,
                      'Type':Lista_type, 
                      'Nclass': Lista_nclass,
                    'label':Lista_label,
                    #'centroid': Lista_centroid,
                    'bbox': Lista_bbox,
                    #'coords':Lista_coords,
                     'intensity_image': Lista_intensity,
                      'mask_image':Lista_mask,
                     'area': Lista_area})             
  return df4    



def pd_info_objects(Lista_filenames, List_quartiles,
                    #Lista_quartile_max,
                    dir_img, dir_binary): 
       
  df_info_init = pd.DataFrame()        
  for file_ in Lista_filenames:    

    pd_x_class= pd_info_features(file_, dir_binary, 
                                 dir_img, List_quartiles,
                                  # Lista_quartile_max
                                )  
    df_info_init = pd.concat([df_info_init, pd_x_class], axis = 0)
        
  return  df_info_init



