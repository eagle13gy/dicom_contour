""" Read, plot and calculate the errors for the thresholding segmentation method
"""

from utilities import *

dres, mIres, mOres=parsing_data_io('final_data')
# use thresholding method to segment the inner contour of the entire data set
# Test a few threshold parameters

for j in range(4,11,1):
    for i in range(dres.shape[0]):
        d1,c1 = dres[i,:,:],mOres[i,:,:]
        m1=segmentation_thres(d1, c1, 0.1*j)
        m1=np.reshape(m1,(1,)+m1.shape)
        if 'mIseg' not in locals():
            mIseg = m1
        else:
            mIseg = np.concatenate((mIseg, m1), axis=0)

    #visualize a few cases with comparision to manual segmentation
    #visualize_dicom_contour_io(dres,mIres,mIseg,3,2)
    #plt.show()

    # calculate the number of the wrongly segmented points w.r.t manual segmentation
    error=abs((mIseg-mIres).astype('float'))
    error_sum=sum(error.flatten())

    # calculate the percentage of the wrongly segmented points w.r.t. manual inner contour
    error_r = error_sum/(sum(mIres.astype('float').flatten()))

    print(error_sum,error_r)

    del mIseg

