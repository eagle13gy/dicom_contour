from parsing import *
import matplotlib.pyplot as plt
from utilities import segmentation_thres

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


# get pixels of blood pool and Myocardium
dc1=dp1[mI1]
dm1=dp1[mO1-mI1]

fig, ax = plt.subplots()
ax.hist((dc1,dm1),bins='auto',color=['red','blue'],label=['Blood Pool','Myocardium'])
ax.legend(prop={'size': 20})
plt.title('Histogram of LV Blood Pool and Myocardium Intensity', fontsize=20)
plt.show()


rI1=segmentation_thres(dp1,mO1,0.9)

# plot the thresholding inner segmented contour with comparison to manually segmented inner contour

plt.figure()
plt.subplot(1,3,1)
plt.imshow(dp1,cmap=plt.gray(),vmin=0, vmax=300)
plt.axis('off')
plt.title('Original image')
plt.subplot(1,3,2)
plt.imshow(dp1+mI1*300,cmap=plt.gray(),vmin=0, vmax=300)
plt.title('Manual segmentation')
plt.axis('off')
plt.subplot(1,3,3)
plt.imshow(dp1+rI1*300,cmap=plt.gray(),vmin=0, vmax=300)
plt.title('Thresholding segmentation')
plt.axis('off')
plt.show()



