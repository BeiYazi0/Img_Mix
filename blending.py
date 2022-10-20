import numpy as np
import scipy.signal


def generatingKernel(a):
    kernel = np.array([0.25 - a / 2.0, 0.25, a, 0.25, 0.25 - a / 2.0])  
    return np.outer(kernel, kernel)


def reduce_layer(image, kernel=generatingKernel(0.4)):
    image=image.astype('float64')     
    kernel=kernel.astype('float64')   
    grad=scipy.signal.convolve2d(image,kernel,boundary='symm',mode='same') 
    image_new=grad[::2,::2]  
    return image_new


def expand_layer(image, kernel=generatingKernel(0.4)):
    image=image.astype('float64')   
    kernel=kernel.astype('float64')  
    r,c=image.shape
    grad=np.zeros([r*2,c*2],dtype='float64')
    grad[::2,::2]=image 
    image_new=scipy.signal.convolve2d(grad,kernel,boundary='symm',mode='same') 
    image_new*=4
    return image_new


def gaussPyramid(image, levels):
    image=image.astype('float64') 
    res=[image]
    for i in range(levels):
        image_new=reduce_layer(res[i]) 
        res.append(image_new)      
    return res


def laplPyramid(gaussPyr):
    n=len(gaussPyr)
    res=[]
    for i in range(1,n):
        pre=gaussPyr[i-1]             
        cur=expand_layer(gaussPyr[i])  
        if pre.shape!=cur.shape:
            cur=cur[:pre.shape[0],:pre.shape[1]] 
        res.append(pre-cur)            
    res.append(gaussPyr[-1])           
    return res


def blend(laplPyrWhite, laplPyrBlack, gaussPyrMask):
    n=len(laplPyrWhite)     
    res=[]
    for i in range(n):
        cur_mask=gaussPyrMask[i].astype("bool") 
        cur_white=laplPyrWhite[i]*cur_mask      
        cur_black=laplPyrBlack[i]*(~cur_mask)   
        res.append(cur_white+cur_black)         
    return res


def collapse(pyramid):
    processimgs=[obj for obj in pyramid] 
    res=processimgs.pop()
    while processimgs:
        p=processimgs.pop()              
        q=expand_layer(res)              
        if p.shape!=q.shape:
            q=q[:p.shape[0],:p.shape[1]] 
        res=p+q                          
    return res
