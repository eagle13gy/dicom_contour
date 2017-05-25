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


def parsing_data_io(filedir):
    """Parse the given DICOM files and inner/outer contour files using the linked CVS
    :param filedir: directory to the DICOM, contour, and CVS files
    :return: 3 numpy arrays, the first containing all the dicoms,
                             the second containing all inner contour masks
                             the third containing all outer contour masks
    """
    ddir=filedir+'/dicoms/'
    cdir=filedir+'/contourfiles/'
    linkdir=filedir+'/link.csv'

    #open link.cvs to get the corrected linked contour/dicoms
    with open(linkdir) as csvfile:
         reader = csv.DictReader(csvfile)
         for row in reader:
            #get contour directory
            contourIdir = cdir + row['original_id'] + '/i-contours/'
            contourOdir = cdir + row['original_id'] + '/o-contours/'
            files = os.listdir(contourOdir)
            for file in files:
                if(file.startswith('IM')):
                    contourOfile=contourOdir+file

                    # get corresponding i-contour file and dicom file directory
                    fsegments=file.split('-')
                    contourIfile=contourIdir+"".join(file[0:12])+'-icontour-manual.txt'

                    id=fsegments[2].lstrip('0')
                    dicomdir=ddir+row['patient_id']+'/'+id+'.dcm'

                    if os.path.isfile(dicomdir) and os.path.isfile(contourIfile): # check if the file exists
                        d1 = parse_dicom_file(dicomdir)
                        dp1=d1['pixel_data']  #get actual numpy pixel data
                        dh, dw = dp1.shape  # get the shape to convert contour into binary mask

                        # concantenate image on the first dimension
                        dp1=np.reshape(dp1,[1,dh,dw])
                        if 'dres' not in locals():
                            dres=dp1
                        else:
                            dres=np.concatenate((dres,dp1),axis=0)

                        cI1 = parse_contour_file(contourIfile) # read i-contour
                        mI1 = poly_to_mask(cI1, dh, dw) # convert contour polygon into boolean mask
                        mI1 = np.reshape(mI1, [1,dh,dw])
                        if 'mIres' not in locals():
                            mIres=mI1
                        else:
                            mIres=np.concatenate((mIres,mI1),axis=0)

                        cO1 = parse_contour_file(contourOfile) # read o-contour
                        mO1 = poly_to_mask(cO1, dh, dw) # convert contour polygon into boolean mask
                        mO1 = np.reshape(mO1, [1,dh,dw])
                        if 'mOres' not in locals():
                            mOres=mO1
                        else:
                            mOres=np.concatenate((mOres,mO1),axis=0)

    return dres, mIres, mOres

def visualize_dicom_contour(dicoms,contours,Nrow,Ncol):
    '''Tool to visualize the first Nrow*Ncol dicom and corresponding contours in a subplot
    :param dicoms: numpy array of dicoms
    :param contour: numpy array of contour boolean masks
    :param Nrow: desired subplot rows
    :param Ncol: desired subplot columns
    '''
    for i in range(Nrow*Ncol):
        plt.subplot(Nrow,Ncol,i+1)
        plt.imshow(np.concatenate((dicoms[i,:,:],dicoms[i,:,:]+contours[i,:,:]*300),axis=1),cmap=plt.gray(),vmin=0, vmax=300)
        plt.axis('off')

def visualize_dicom_contour_io(dicoms, contours1, contours2, Nrow, Ncol):
    '''Tool to visualize the first Nrow*Ncol dicom and corresponding contours in a subplot
    :param dicoms: numpy array of dicoms
    :param contour: numpy array of contour boolean masks
    :param Nrow: desired subplot rows
    :param Ncol: desired subplot columns
    '''
    for i in range(Nrow * Ncol):
        plt.subplot(Nrow, Ncol, i + 1)
        plt.imshow(np.concatenate((dicoms[i, :, :], dicoms[i, :, :] + contours1[i, :, :] * 300,
                                   dicoms[i, :, :] + contours2[i, :, :] * 300), axis=1),
                                   cmap=plt.gray(), vmin=0, vmax=300)
        plt.axis('off')

def segmentation_thres(image, contourO, thres=1):
    '''Tool to segment the inner contour given the outer contour
    :param image: numpy array of one image
    :param contourO: numpy array of contour boolean masks
    :param thres:  percentage threshold to control the performance, default is 1
    :return segmented inner contour mask
    '''

    # get the mean pixel value inside the outer contour region
    regionO = image[contourO]
    meanR = sum(regionO) / len(regionO)
    meanR = meanR * thres  # thres variable control the threshold value w.r.t to mean value

    # mask out the myocardium part based on the threshold value
    contourI = contourO
    for index, c in np.ndenumerate(contourI):
        if (c == True):
            if (image[index] < meanR):
                contourI[index] = False

    return contourI


# unit test to visualize the loaded dicom, and dicom + inner/outer contours
#dres, mIres, mOres=parsing_data_io('final_data')
#visualize_dicom_contour_io(dres,mIres,mOres,3,2)
#plt.show()