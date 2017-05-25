""" Read, plot and calculate the errors for the thresholding segmentation method
"""

from utilities import *
dres, mIres, mOres=parsing_data_io('final_data')

for j in range(3,10,1):
    for i in range(dres.shape[0]):
        d1,c1 = dres[i,:,:],mOres[i,:,:]
        m1=segmentation_thres(d1, c1, 0.1*j)
        m1=np.reshape(m1,(1,)+m1.shape)
        if 'mIseg' not in locals():
            mIseg = m1
        else:
            mIseg = np.concatenate((mIseg, m1), axis=0)

    #visualize_dicom_contour_io(dres,mIres,mIseg,3,2)
    #plt.show()

    error=abs((mIseg-mIres).astype('float'))

    error_sum=sum(error.flatten())
    error_r = error_sum/(sum(mIres.astype('float').flatten()))

    print(error_sum,error_r)

    del mIseg

