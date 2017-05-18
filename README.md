# dicom_contour
Pipeline to read paired dicom and contours
============================================================

Code Structure
--------------
### Demo scripts
**read_single.py**
unit test to read one dicom/contour file to verify if the read functions are working
plot the dicom and corresponding contour after successful read to check if the ROI is reasonable:

![alt text](https://github.com/eagle13gy/dicom_contour.git/master/single_res.png)



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
