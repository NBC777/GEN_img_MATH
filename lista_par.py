from utils import *
#from libraries import *
from info_prm  import *
import cv2


random.seed(10) 


def  interx_(half_1,half_2, dir_lista2x, dir_out, m2x):

    listax2 = half_1 + half_2  

    i=0       
    sumxx=0               

    Lfn_delete=[]         
    Lplot_delete = []    

    while i < m2x:    
        fname1x = half_1[i]       
        fname2x = half_2[i]         
        filename_2 = dir_lista2x + fname2x    

        img2_ = Image.open(filename_2)            
        img2 = np.asarray(img2_)                                  
        img2xx = np.where(img2 != 0, 1,0)                                         
        filename_1i2 = dir_lista2x +fname1x 
      
        img1_ = Image.open(filename_1i2)
        img1 = np.asarray(img1_) 
   
        img1xx = np.where(img1 != 0, 1,0)
                
        bitwiseAnd = cv2.bitwise_and(img1xx, img2xx)  
        
        if (bitwiseAnd == 0).all():                   

            bitwiseOr =  img1 + img2
            img_pil = Image.fromarray(bitwiseOr.astype('uint8'), mode='P') 
            img_pil.putpalette(palette_from_dict(colors_dict))
            fname_1 = fname1x.replace(".png", "")
            fname_2 =fname2x # filename de Lista_imgs
            filenamex = fname_1 + '.' + fname_2  
            img_pil.save(dir_out + filenamex)  
            #print('FILENAMEx:>>', filenamex)
     
            sumxx +=1
            nfile = [fname1x, fname2x]
            Lfn_delete += nfile # imgs1x que se intersectam.     
            Lplot_delete += [filenamex]#img2x que se interwectam;.
             
        else:  
   
              
            pass           

        #print('Lfn_  ANTES  ::>>', set(Lfn_delete))
        listax2 = list(set(listax2).difference(set(Lfn_delete)))
                          
        i+=1

    return Lfn_delete, Lplot_delete 

  
def par_inter(listax2, dir_lista2x, dir_out):
    #rand_listx2 = random.sample(listax2, value*len(listax2))    
    m2x= len(listax2)//2  
    half_1 = listax2[:m2x]
    half_2 = listax2[m2x:]

    Lfn_delete, Lplot_delete  = interx_(half_1,half_2, m2x)
    
    return Lfn_delete, Lplot_delete  
           
      
# 

#####
###   FINAL
####
def spar2XY(listax2_, dir_lista2x, dir_out, s):
    """ 
    Funcion que intersecta imagens 2x. 
    """
    Lx2 = listax2_       

    F2x=[]
    F4x=[]    

    Lmss = Lx2

    for rdn in range(s):

        m2x = len(Lmss)//2    

        half_1 = Lmss[:m2x]
        #print('len de half_1:>>', len(half_1))
        half_2=Lmss[m2x:]
        f2x, f4x = interx_(half_1,half_2,dir_lista2x, dir_out, m2x)  

        F2x.append(f2x)
        F4x.append(f4x)
    
        #print('listax2::>>>', Lx2)    
         
        list_result1 = [item for item in Lx2  if item not in  f2x]
        #[item for item in listax2 if not item in f2x]
   
   
        list_result2 = list_result1 + f4x      
        #print('list_result2', list_result2)
        list_result = list_result2# [item for sublist in list_result2  for item in sublist]
 
        g=0    
        for itm in Lx2:    
            if itm  in f2x:  
                
                #print('file to remove::>>', itm)
                os.remove(os.path.join(dir_lista2x , itm))
                g+=1
            else:

                #print('Foram apagados arquivos')# {} arquivos:>', format(len())
                pass  


        Lx2 = list_result

        Lmss = f4x  
    
    return list_result           
          
             

                
           

            
      
    