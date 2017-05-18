import csv
import os
from parsing import *
import matplotlib.pyplot as plt

def parsing_data(filedir):
    """Parse the given DICOM files and contour files using the linked CVS
    :param filedir: directory to the DICOM, contour, and CVS files
    :return: 2 numpy arrays, the first containing all the dicoms, and the second containing all the contour masks
    """
    ddir=filedir+'/dicoms/'
    cdir=filedir+'/contourfiles/'
    linkdir=filedir+'/link.csv'

    #open link.cvs to get the corrected linked contour/dicoms
    with open(linkdir) as csvfile:
         reader = csv.DictReader(csvfile)
         for row in reader:
            #get contour directory
            contourdir = cdir + row['original_id'] + '/i-contours/'
            files = os.listdir(contourdir)
            for file in files:
                if(file.startswith('IM')):
                    contourfile=contourdir+file
                    # read contour file into coord list
                    c1=parse_contour_file(contourfile)

                    # get corresponding dicom number
                    fsegments=file.split('-')
                    id=fsegments[2].lstrip('0')
                    dicomdir=ddir+row['patient_id']+'/'+id+'.dcm'
                    d1 = parse_dicom_file(dicomdir)
                    if d1 is not None:
                        dp1=d1['pixel_data']  #get actual numpy pixel data
                        dh, dw = dp1.shape  # get the shape to convert contour into binary mask

                        # concantenate image on the first dimension
                        dp1=np.reshape(dp1,[1,dh,dw])
                        if 'dres' not in locals():
                            dres=dp1
                        else:
                            dres=np.concatenate((dres,dp1),axis=0)

                        m1 = poly_to_mask(c1, dh, dw) # convert contour polygon into boolean mask
                        m1 = np.reshape(m1, [1,dh,dw])
                        if 'mres' not in locals():
                            mres=m1
                        else:
                            mres=np.concatenate((mres,m1),axis=0)
    return dres, mres


def visualize_dicom_contour(dicoms,contours,Nrow,Ncol):
    '''Tool to visualize the first Nrow*Ncol dicom and corresponding contours in a subplot
    :param dicoms: numpy array of dicoms
    :param contour: numpy array of contour boolean masks
    :param Nrow: desired subplot rows
    :param Ncol: desired subplot columns
    '''
    for i in range(Nrow*Ncol):
        plt.subplot(Nrow,Ncol,i+1)
        plt.imshow(np.concatenate((dicoms[i,:,:],dicoms[i,:,:]+contours[i,:,:]*200),axis=1),cmap=plt.gray(),vmin=0, vmax=300)
        plt.axis('off')

# unit test to visualize the loaded dicom, and dicom + contour
#dres, mres=parsing_data('final_data')
#visualize_dicom_contour(dres,mres,2,3)
#plt.show()