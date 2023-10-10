import numpy as np
import random

  

rows = 7
columns=8
np_matrix = np.random.rand(rows, columns)
np2 = np.random.rand(rows, columns)
print('random matrix:', np_matrix.shape)

x, y = np_matrix.shape
b= np.empty(np_matrix.shape, dtype=int)

#print('max>>', max(np_matrix.shape))



def search_new_xy(theta,w,h,w0,h0, Trs, corner):
  #theta_list = [90,180,270]

  #theta = random.choice(theta_list)

  if theta ==90:
    w1, h1= h0, w0
    
    if h - w0 < Trs or corner:
      x=0
      y= w - h0
    else:
      x = random.randrange(h-w0)
      y=w -h0

    
  if theta == 180:
    w1, h1 = w0, h0

    if w-w0 < Trs or corner:
      x=0
      y=0

    else:
      x=0
      y = random.randrange(w-w0)

  elif theta== 270:
    w1,h1 = h0, w0

    if h - h0 < Trs or corner:
      x = h - w0
      y=0
    else:
      y=0
      x= random.randrange(h-w0)

  x_final = x + h1
  y_final = y + w1

  return x, y, x_final, y_final


bool= False

if  bool:
  print('Dentrooooo do IF')

else:

  print('NOooo  ELSE')




