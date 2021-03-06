

#convolution I*K

from skimage.exposure import rescale_intensity
import numpy as np
import argparse
import cv2

def convolve(image , K):
    (iH ,iW) = image.shape[:2]
    (kH , kW) = K.shape[:2]
    
    pad =(kW-1)//2
    
    image =cv2.copyMakeBorder(image ,pad,pad,pad,pad , cv2.BORDER_REPLICATE)
    
    output =np.zeros((iH,iW) , dtype ="float")
    
    for y in np.arange(pad ,  iH+pad):
        for x in np.arange(pad , iW+pad):
            #defining ROI
            
            roi =image[y-pad: y+pad+1 , x-pad:x+pad+1]
            
            k =(roi*K).sum()
            
            output[ x-pad , y-pad] =k
            
            output = rescale_intensity(output, in_range=(0,255))
            output = (output*255).astype("uint8")
            
            
            return output
        


# parsing the arguments

ap = argparse.ArgumentParser()

ap.add_argument("-i", "--image", required = True , help ="path to the input image")
args = vars(ap.parse_args())



smallBlur = np.ones((7,7), dtype = "float")*(1.0/(7*7))
largeBlur = np.ones((21,21),  dtype ="float")*(1.0/(21*21))

sharpen = np.array(( 
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0]), dtype="int")

laplacian = np.array((
    [0, 1, 0],
    [1, -4, 1],
    [0, 1, 0]), dtype="int")

sobelX = np.array(( 
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1]), dtype="int")

sobelY = np.array(( 
    [-1, -2, -1],
    [0, 0, 0],
    [1, 2, 1]), dtype="int")
emboss = np.array(( 
    [-2, -1, 0],
    [-1, 1, 1],
    [0, 1, 2]), dtype="int")


kernelBank = (
    ("small_blur" , smallBlur),
    ("large_blur" ,largeBlur),
    ("sharpen" ,sharpen),
    ("laplacian" , laplacian),
    ("sobel_x" ,sobelX),
    ("sobel_y" ,sobelY),
    ("emboss" ,emboss))


#convert the image to greyscale
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


#loop over the kernels
for (kernelName , k) in kernelBank:
    print("image is loading{}".format(kernelName))
    convolveOutput = convolve(gray,k)
    opencvOutput = cv2.filter2D(gray , -1, k)
    
    
    #show the output images
    cv2.imshow("Orignal",  gray)
    cv2.imshow("{}-convolve".format(kernelName), convolveOutput)
    cv2.imshow( "{}-gray".format(kernelName), opencvOutput)
    cv2.waitKey(0)
    cv2.destroyAllWindows()





    
    
    

    
    
    
    
    
    
    
    
    
    
    
    


# In[ ]:





# In[ ]:




