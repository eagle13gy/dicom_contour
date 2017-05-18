from parsing import *
import matplotlib.pyplot as plt

# unit test to read one dicom/contour file to verify if the read functions are working
# plot the dicom/contour after successful read

dicomdir='final_data/dicoms/SCD0000101/48.dcm'
contourdir='final_data/contourfiles/SC-HF-I-1/i-contours/IM-0001-0048-icontour-manual.txt'

d1=parse_dicom_file(dicomdir)
dp1=d1['pixel_data']

dh, dw=dp1.shape
c1=parse_contour_file(contourdir)
m1=poly_to_mask(c1,dw,dh)

#m1=m1.astype('float32')
#print(m1[100])
#print(np.amax(dp1))
#print(dp1[100])

# plot the dicom and the dicom+contour
plt.figure()
plt.subplot(1,2,1)
plt.imshow(dp1,cmap=plt.gray(),vmin=0, vmax=300)
plt.axis('off')
plt.subplot(1,2,2)
plt.imshow(dp1+m1*200,cmap=plt.gray(),vmin=0, vmax=300)
plt.axis('off')
plt.show()


