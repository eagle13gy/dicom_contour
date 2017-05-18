# dicom_contour
Pipeline to read paired dicom and contours
============================================================

Code Structure
--------------
### Part 1
**read_single.py**: 
unit test to read one dicom/contour file to verify if the read functions are working
plot the dicom and corresponding contour after successful read to check if the ROI is reasonable:

![alt text](https://github.com/eagle13gy/dicom_contour/blob/master/single_res.png)

**link_data.py**:
*parsing_data(filedir)*:Parse the given DICOM files and contour files using the linked CVS
return 2 numpy arrays, 1 containing all the dicoms, and the other containing all the contour masks

*visulize_dicom_contour(dicoms,contours,Nrow,Ncol)* : a small utility to visulize first few paired dicom and contour using subplots

![alt text](https://github.com/eagle13gy/dicom_contour/blob/master/multi_res.png)




### Functions: 
**conc2Ktrans.m**: 
	Convert contrast concentration to TK parameter maps.  
**conc2sig.m**: 
	Convert contrast concentration to signal (images).  
**genRGA.m**: 
	Generate randomized golden-angle radial sampling pattern.  
**Kt_Vp_SEN.m**: 
	Alternatively reconstruct Ktrans and Vp maps using l-bfgs.  
**Ktrans2conc.m**: 
	Convert Ktrans maps to contrast concentration.  
**sig2conc2.m**: 
	Convert signal (images) to contrast concentration.  
**Ktrans2sig_sen_WT.m**: 
	Cost and gradient calculation for the objective function for Ktrans.  
**Vp2sig_SEN_WT.m**: 
	Cost and gradient calculation for the objective funciton for Vp.  
**SAIF_p.m**: 
	Generate population-averaged AIF.  
