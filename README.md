Pipeline to read paired dicoms and contours
============================================================
Yi Guo


Part 1: Parse the o-contours
--------------
### utilities.py: 
Organized data read and image visualization functions in this file.  <br />
**parsing_data_io(filedir)**:
Based on previous version, parse the given DICOM files and inner/outer contour files using the linked CVS.
Return 3 numpy arrays, the first containing all the dicoms, the second containing all inner contour masks, the third containing all outer contour masks. The first dimension is used to concantenate the images/masks. 
Only return the images/contours that have both inner and outer contours.

**visualize_dicom_contour_io(dicoms, contours1, contours2, Nrow, Ncol)**:
Based on previous version, visualize the three images: original, and 2 contour-overlaped images for easy comparison. 

Using the above functions to visualize the correct parsing of both inner and outer contours for a few images:
![alt text](https://github.com/eagle13gy/dicom_contour/blob/master/figures/Outer_Contour.png)


### Questions:
#### Discuss any changes that you made to the pipeline you built in Phase 1, and why you made those changes?
The new version now reads outer contour first, then search for the existance of corresponding inner contour and image. I added an "if" statement to first check the existance of those files, instead of checking the return of the parse_dicom_file function is "NONE" or not. This should be a safer and faster way to load the data. Moreover, the function reads the image and the contours only after all three elements of a data set exist. 

Part 2: Heuristic LV Segmentation approaches
--------------

### read_single.py: 
Plot the histogram of the LV blood pool and myocardium intensity:
![alt text](https://github.com/eagle13gy/dicom_contour/blob/master/figures/histogram.png)

It is obviously that an thresholding method based on intensity should work to segment the blood pool, although not perfectly for some pixels.

### segmentation_thres(image, contourO, thres=1) (in utilities.py): 
Test a simple thresholding scheme to segment the inner contour given the outer contour. The mean image intensity inside the outer contour is calculated first. Then based on the intensity, the blood pool should have higher value, while the myocardium should have lower value. The segmentation is then based on the mean value times some percentage threshold (default to be 1) to control the performance. A simple test is done on one image first, and visualized with comparision to manual segemented result (in read_single.py):

![alt text](https://github.com/eagle13gy/dicom_contour/blob/master/figures/Single_Thres.png)

In this one data set, the performance is rather good. 

### statistical_analysis.py:
Use the above method to segment the entire data set, visualize a few data set with comparision to manual segmentation, and show some results with different threshold parameter selections:

![alt text](https://github.com/eagle13gy/dicom_contour/blob/master/figures/Thres_1.0.png)

![alt text](https://github.com/eagle13gy/dicom_contour/blob/master/figures/Thres_0.7.png)

The simple thresholding method performs well for certain cases, but not so well for a few cases with blurred boundaries. The threshold can affect the performance, but this parameter needs manual tuning. 

To quantitatively evaluate the performance, the total number of wrongly segmented points, and the percentage of these points w.r.t manual inner contours were calcualted. Below are some results for a range of threshold values:

|Thres |Total   |Percentage|
| -----|:------:| -----:|
|0.4   | 30026  | 48.45%|
|0.5   | 20855  | 33.65%|
|0.6   | 17984  | 29.02%|
|0.7   | 17891  | 28.87%|
|0.8   | 20316  | 32.78%|
|0.9   | 28763  | 46.42%|
|1.0   | 46058  | 74.33%|


### Questions: 
#### Do you think that any other heuristic (non-machine learning)-based approaches, besides simple thresholding, would work in this case? Explain?

1. Many classic methods should work. One method is region growing, where the seed can be chosen based on the center of the outer contour. 
The region can grow into neighbouring points based on the similarity between the seed and the neighbouring points (difference in intensity). 
Some threshold can control the tolerance for the difference, and the growing region can be bounded by the outer contour.
Based on the histogram, the region growing method can resolve some of the overlaping pixels between blood pool and myocardium, since a neighbouring condition is enforced other than pure intensity-based thresholding. 

I couldn't find a good open source region grow method for python. I tried one data set using Matlab, below is the result:
![alt text](https://github.com/eagle13gy/dicom_contour/blob/master/figures/region_grow.png)

2. Also methods based on the gradient (boundary) of the images should work well, since there's some clear boundary between the blood pool and myocardium. Watershed method, which resembles region grow, but utilizes the boundary information, should work well in this case.


