
from  preprocessing_   import preproc
from gen_annotations  import gen_all_masks
from gen_imgs_1class  import gen_imgs_one_class
from multiple_annotations  import multiples_ann    
from gen_imgs_nclasses  import gen_images_nclasses
from gen_missing_imgs  import completing_imgs



Kwargs = {'preproc': 'a=None'}  

def parse_args():
    parser=argparse.ArgumentParser(description="a script to do stuff")
    #parser.add_argument("R1_file")
    args=parser.parse_args()

    print("the inputs are:")
    for arg in vars(args):
        print("{} is {}".format(arg, getattr(args, arg)))

    return args

#def process_files(things):
#    print("this is the process files function")
#    print(things.R1_file)
  

def main(preproc, gen_all_masks, gen_imgs_one_class,
         multiples_ann, gen_images_nclasses,
         completing_imgs):
        #foo, bar, **kwargs):
    print('==================> Called myscript main:')

    #print("this is the main function")
    #inputs=parse_args()
    #print(inputs.R1_file)
    #process_files(inputs)
    print('===================> preproc:>>')
    preproc()
    print('====================> gen_all_masks')
    gen_all_masks()
    print('=====================> gen_imgs_one_class')
    gen_imgs_one_class()
    print('=====================> multiple_ann')
    multiples_ann()
    print('======================> gen_images_nclasses')
    gen_images_nclasses()
    print('=======================> completingg...')
    completing_imgs()

        

#if __name__ == '__main__':
#    args = p.parse_args()
#    main(**vars(args))
  

if __name__ == '__main__':
    #args = p.parse_args()
    #main(**vars(args))
    main(preproc, gen_all_masks, gen_imgs_one_class, 
         multiples_ann, gen_images_nclasses,
         completing_imgs)

