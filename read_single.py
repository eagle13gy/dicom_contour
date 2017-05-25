from parsing import *
import matplotlib.pyplot as plt

# unit test to read one dicom/contour file to verify if the read functions are working
# plot the dicom/contour after successful read

dicomdir='final_data/dicoms/SCD0000101/59.dcm'
contourIdir='final_data/contourfiles/SC-HF-I-1/i-contours/IM-0001-0059-icontour-manual.txt'

contourOdir='final_data/contourfiles/SC-HF-I-1/o-contours/IM-0001-0059-ocontour-manual.txt'

d1=parse_dicom_file(dicomdir)
dp1=d1['pixel_data']

dh, dw=dp1.shape

cI1=parse_contour_file(contourIdir)
mI1=poly_to_mask(cI1,dw,dh)

cO1=parse_contour_file(contourOdir)
mO1=poly_to_mask(cO1,dw,dh)

def segmentation_thres(image, contourO,thres=1):
    '''Tool to segment the inner contour given the outer contour
    :param image: numpy array of one image
    :param contourO: numpy array of contour boolean masks
    :param thres:  percentage threshold to control the performance, default is 1
    :return segmented inner contour mask
    '''

    # get the mean pixel value inside the outer contour region
    regionO=image[contourO]
    meanR=sum(regionO)/len(regionO)
    meanR=meanR*thres # thres variable control the threshold value w.r.t to mean value

    # mask out the myocardium part based on the threshold value
    contourI=contourO
    for index, c in np.ndenumerate(contourI):
        if(c==True):
            if(image[index]<meanR):
                contourI[index]=False

    return contourI


rI1=segmentation_thres(dp1,mO1,0.9)

# plot the thresholding inner segmented contour with comparison to manually segmented inner contour

plt.figure()
plt.subplot(1,3,1)
plt.imshow(dp1,cmap=plt.gray(),vmin=0, vmax=300)
plt.axis('off')
plt.subplot(1,3,2)
plt.imshow(dp1+rI1*300,cmap=plt.gray(),vmin=0, vmax=300)
plt.axis('off')
plt.subplot(1,3,3)
plt.imshow(dp1+mI1*300,cmap=plt.gray(),vmin=0, vmax=300)
plt.axis('off')
plt.show()

