from utils  import *   
from lista_par import *
import glob 
  

_PATH = '/home/nbc10/Documentos/Dataset_/'

      
def making_pd_fn3(pwd, M, nclass):
  """    
  Pandas which columns and rows is filename of the random mask image 
  """      
  df_empty = pd.DataFrame(index=range(0,M), dtype = 'str')
  csv_files = glob.glob(os.path.join(pwd, "*.csv"))
      
  for file_ in csv_files:
    dfx = pd.read_csv(file_, usecols=['Lfilename']).replace(r'\s+',np.nan, regex=True).replace('',np.nan)
    #.fillna(0)  
    ffname = file_.split('.')[0]
    name_col = 'classe'+str(ffname[-1])
    dfx.columns = [name_col]
    df_empty = pd.concat([df_empty, dfx], axis=1)

    df_empty = df_empty.reindex(natsorted(df_empty.columns), axis=1)

  return df_empty   
     


def intersection_Lxj(dir_in, plot_dir, pd_Lxj_):
    """
    Func to look for labels images with intersection 
    in one line
    plot_dir:  folder to save the file.
    dir_in : folder onde a mask image localiza-se.
    pd_Lxj : 
    """

          
    Lista_to_remove = []  

    pd_Lxj= pd_Lxj_.squeeze()
      
    New_list_ = pd_Lxj[pd_Lxj.notnull()]#.all(1)        

    New_list = New_list_.tolist()
    s= len(New_list)
        
    Lista_to_remove=[]
      
    for j in range(s//2): 
      
        file_1 = New_list[2*j]  

        fname_1= file_1.split('.')[0]
        c = int(fname_1[-1])
        img1_ = Image.open(dir_in[c-1] + file_1)
        img1_arr = np.asarray(img1_) 
        img1xx = np.where(img1_arr != 0, 1,0)

        file_2 = New_list[2*j + 1]    
        fname_2= file_2.split('.')[0]
        d = int(fname_2[-1])
        img2_ = Image.open(dir_in[d-1] + file_2)
        img2_arr = np.asarray(img2_) 
      
          
        img2xx = np.where(img2_arr != 0, 1,0)      

        bitwiseAnd = cv2.bitwise_and(img1xx, img2xx)  
        if (bitwiseAnd == 0).all():
      
          bitwiseOr = cv2.bitwise_or(img1_arr, img2_arr)     
          img_pil = Image.fromarray(bitwiseOr.astype('uint8'), mode='P') 
          img_pil.putpalette(palette_from_dict(colors_dict))
          new_fname = fname_1 + '.' + fname_2 + '.png'
        
          img_pil.save(plot_dir + new_fname)    
      
          Lista_to_remove.append(new_fname)

        else: 
          ##print('Caso contrario en Interseccion. No hay nova imagem::>>') 
          continue                  

   
    return Lista_to_remove   
       

def  XZ0(Num_imgs, value, pd_infox, plot_dir, dir_in):
  """
  function that busca intercessões (2xclass)  en un 
  grupo de index  en pandas.
  Index_pandas = Lindex        
  """ 
  print('Dentro de XZ0')         
    
  n_max = max(Num_imgs)
  #k1 = round(value*n_max) 
  k1 = n_max             
    
  pd_info = pd_infox.copy(deep=True)      

  nrand= random.sample(pd_info.index.tolist(), k= int(k1)) #amostra de index 

  new_pd_info = pd_info.loc[pd_info.index.isin(nrand)]  
    
  new_pd_info.reset_index(inplace=True)
  new_pd_info= new_pd_info.rename(columns = {'index':'IDX'})        

  _PATH = '/home/nbc10/Documentos/Dataset_/'       

            
  out_a1 = new_pd_info.to_csv(_PATH + 'new_pd_infoXY.csv')   
          

  h=0                       
  Lfirst =[]                               


  col2 = ['classe'+str(i) for i in range(1,7)]
                          

  for idx in nrand:

    pd_idx = new_pd_info.loc[new_pd_info.IDX==idx, col2]

    Nan_= pd_idx.isnull().sum().sum()    
       
    if Nan_ <= 4:                         
              
      Lista_except = intersection_Lxj(dir_in, plot_dir, pd_idx)

      h += len(Lista_except)       
             
    else:    

      Lista_except = []  

    Lfirst.append(Lista_except)   
 
  nLfirst =  [item for sublist in Lfirst for item in sublist]          
        
  return   nLfirst    #Lista TOTAL   imags 2x 

###   FINAL  ==== 
###################
##################   
                  
def  WXZ(value,pd_info, plot_dir,dir_in, nclass,  Num_imgs):  

  print('  Dentro  de  WXZ   function ======')          
  """
  Function that search  multiples interseções de images
  que são interseções na etapa anterior>>>        

  plot_dir: folder onde estarão as mascaras (DATAx_2)
  dir_in: onde a mascara está. LDIR_LABELS
  pd_value: 
  Num_imgs:= Lnum_imgs (Lista de numeros de images en cada classe.)
  pd_info :  pd  about  filenames of all in folders:
  """


  X2_ = XZ0(Num_imgs, value, pd_info, plot_dir, dir_in)

  print('Len de Lrm0:>>', len(X2_))

  # GENERATE  2X:                     
  X2 = X2_.copy()  
  
  Lista_plots = X2  


  # GENERATE  NX  PAR:
  s=2
  files_2x_4x  = spar2XY(Lista_plots, plot_dir, plot_dir, s)

  nn=  len(files_2x_4x)        
  #print('Len de  arquivos  de interseccion par x2x4  Total::nn', nn)    

  flat_listX = nested_List_flatten(files_2x_4x)   
 
  #         
  nrand2= random.sample(pd_info.index.tolist(), k= int(np.ceil(2*nn/nclass)))   
  
  new_pd = pd_info.iloc[nrand2]               
  pd_matrix = new_pd.to_numpy()                         
  cleanedList = [x for x in pd_matrix.ravel() if str(x) != 'nan'][:nn] 
 
  Lista_randx =[item for item in cleanedList if item not in flat_listX]#nflat_list_remove]  
    
  nnn = len(Lista_randx)       
  
  nm = min(nn, nnn)                    

  Lista_plotsxy =files_2x_4x[:nm]    

  Lfiles1x = []
  Lplots = []    
    
  sumxx =0
  i = 0      
  Lf2x4x = []         
           
  while i < nm:  
          
    fname1x =  Lista_randx[i]         
    fn1_c =  fname1x.split('.')[0][-1]

    fname2x = Lista_plotsxy[i]     
 
    fn2xy = fname2x.split('.')[:-1]      

          
    fn2_c =[ h[-1]  for h in fn2xy] 

        
    if  fn1_c  in fn2_c: 
 
      pass      
          
    else:

      filename_2 = plot_dir + fname2x 
      img2_ = Image.open(filename_2)        

      img2 = np.asarray(img2_)       
         
      img2xx = np.where(img2!= 0, 1,0) 

      filename_1i2 = dir_in[int(fn1_c)-1] +fname1x 
             
      img1_ = Image.open(dir_in[int(fn1_c)-1] + fname1x)
      img1 = np.asarray(img1_) 
      img1x = np.where(img1 !=0, 1,0)
       
      bitwiseAnd = cv2.bitwise_and(img1x, img2xx)  
      
      if (bitwiseAnd == 0).all():          


        bitwiseOr = img1 + img2
        img_pil = Image.fromarray(bitwiseOr.astype('uint8'), mode='P') 
        img_pil.putpalette(palette_from_dict(colors_dict))
        fname_1 = fname1x.replace(".png", "")
        fname_2 =fname2x # filename de Lista_imgs
        filenamex = fname_1 + '.' + fname_2  
        img_pil.save(plot_dir + filenamex)  

        sumxx +=1
      
        Lfiles1x.append(fname1x)      

        Lplots.append(filenamex)   

        Lf2x4x.append(fname2x)  
                          
      else:  

        pass             
        

    i+=1

  nLfiles1x =  Lfiles1x +  flat_listX 
  #print(' Len de  total  de nLfiles1x : >>>',len(nLfiles1x))
  nLplots = Lplots + files_2x_4x      

  fn_plots_rm = [ plot_dir + nfile  for nfile  in Lf2x4x] 
  k1= 0          
  for file_ in fn_plots_rm:                     
      os.remove(file_)  
      k1 +=1  

  print('Foram eliminados  {}   arquivos::>>'.format(k1))
  

  print('FIM  DO   XZ   ======================')      

  return nLfiles1x  


       


       

        