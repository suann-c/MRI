import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import SimpleITK as sitk
from PIL import Image
import imageio
import skimage.io as skio
import skimage.color as color
import cv2
import os

import alignment

#Given an opened nii gz file, this function will save all the separate images into a data dir
def saveImages(t1Img):
    # and access the numpy array:
    t1 = sitk.GetArrayFromImage(t1Img)
    for slice in range(t1.shape[2]):
        print("writing slice")
        filename = 'mriImages/mri%d.png'% slice
        skio.imsave(filename, t1[:, :, slice])


#Given an opened nii gz file, this function will use SITK's sobel filter to auto crop
def sobelAutocrop(sitkImg):
    # Parse input data frames into frames that can be aligned
    # similar to hw2 to do Sobel filter.
    sobelFilter = sitk.SobelEdgeDetectionImageFilter()
    # float_image = sitk.Cast(sitk_t1, sitk.sitkFloat32)
    sobelEdges = sobelFilter.Execute(sitkImg)
    sobelArr = sitk.GetArrayFromImage(sobelEdges)
    for slice in range(sobelArr.shape[2]):
        filename = 'sobel/mri%d.png' % slice
        # TODO: ACTUALLY DO SOBEL CROPPING. RIGHT NOW IT'S JUST SOBEL EDGE DETECTION
        skio.imsave(filename, sobelArr[:, :, slice])
    #plt.imsave("data/10.png", sitk.GetArrayFromImage(sobelEdges[:, :, 10]))


def mergeAlignment(inputDir):
    i = 0
    totalLen = 175
    for env in os.listdir(inputDir):
        #print(inputDir+"mri"+str(i)+".png")
        im1 = skio.imread(inputDir+"mri"+str(i)+".png") #read in curr image and curr image+1
        im2 = skio.imread(inputDir+"mri"+str(i+1)+".png")

        aligned = alignment.ssdAlign(im2, im1)
        alignedIm2 = np.roll(im2, aligned[0], axis=(0, 1))

        #resave the images
        filename1 = "aligned/%d.png" % (i)
        filename2 = "aligned/%d.png" % (i+1)
        if (i == 0):
            skio.imsave(filename1, im1)
            i += 1
            continue
        else:
            skio.imsave(filename1, im1)
            skio.imsave(filename2, alignedIm2)

        if (i == totalLen):
            break
        i += 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # A path to a T1-weighted brain .nii image:
    t1_fn = 'data/sub-047EPKL011005_ses-1_anat_sub-047EPKL011005_ses-1_T1w.nii.gz'
    # Read the .nii image containing the volume with SimpleITK:
    sitk_t1 = sitk.ReadImage(t1_fn)
    #saveImages(sitk_t1) #uncomment this line to save all the image files into a data directory

    #Use sobel filter to autocrop
    #sobelAutocrop(sitk_t1)

    #Run L2 norm distance between each of the slices once autocrop has happened
    mergeAlignment('sobel/')


