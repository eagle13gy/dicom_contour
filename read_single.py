from parsing import *
import matplotlib.pyplot as plt
from regiongrowing import *

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

def segmentation_thres(image, contourO,thres):
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

#    return region



def make_circle1(c1):
    xcor = sum(coor[0] for coor in c1)/len(c1)
    ycor = sum(coor[1] for coor in c1)/len(c1)

    RR=[]
    for coor in c1:
        RR.append(pow(pow(coor[0]-xcor,2)+pow(coor[1]-ycor,2),0.5))

    RR=sum(RR)/len(c1)

    return (xcor,ycor,RR)

print(make_circle1(cI1))


#rI1=segmentation_thres(dp1,mO1,0.9)

rI1=region_growing(dp1/3,(130,138),0.5)


#m1=m1.astype('float32')
#print(m1[100])
#print(np.amax(dp1))
#print(dp1[100])

# plot the dicom and the dicom+contour

plt.figure()
plt.subplot(1,3,1)
plt.imshow(dp1,cmap=plt.gray(),vmin=0, vmax=300)
plt.axis('off')
plt.subplot(1,3,2)
plt.imshow(rI1*300,cmap=plt.gray(),vmin=0, vmax=300)
plt.axis('off')
plt.subplot(1,3,3)
plt.imshow(dp1+mI1*300,cmap=plt.gray(),vmin=0, vmax=300)
plt.axis('off')
plt.show()

