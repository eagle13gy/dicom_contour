Pipeline to read paired dicoms and contours
============================================================
Yi Guo


Part 1: Parse the o-contours
--------------
### utilities.py: 
Organized data read and image visualization functions in this file. 
**parsing_data_io(filedir)**:
Based on previous version, parse the given DICOM files and inner/outer contour files using the linked CVS.
Return 3 numpy arrays, the first containing all the dicoms, the second containing all inner contour masks, the third containing all outer contour masks. The first dimension is used to concantenate the images/masks. 
Only return the images/contours that have both inner and outer contours.

**visualize_dicom_contour_io(dicoms, contours1, contours2, Nrow, Ncol)**:
Based on previous version, visualize the three images: original, and 2 contour overlaped images for easy comparison. 

Using the above functions to visualize the correct parsing of both inner and outer contours for a few images:
![alt text](https://github.com/eagle13gy/dicom_contour/blob/master/figures/Outer_Contour.png)


### Questions:
#### Discuss any changes that you made to the pipeline you built in Phase 1, and why you made those changes?
The new version now reads outer contour first, then search for the existance of corresponding inner contour and image. I added an "if" statement to first check the existance of those files, instead of checking the return of the parse_dicom_file function is "NONE" or not. This should be a safer and faster way to load the data. Moreover, the function reads the image and the contours only after all three element of a data set exist. 


Part 2: Heuristic LV Segmentation approaches
--------------
### segmentation_thres(image, contourO, thres=1) (in utilities.py): 
Test a simple thresholding scheme to segment the inner contour given the outer contour. The mean image intensity inside the outer contour is calculated first. Then based on the intensity, the blood pool should have higher value, while the myocardium should have lower value. The segmentation is then based on the mean value times some percentage threshold (default to be 1) to control the performance. A simple test is done on one image first, and visualize with comparision to manual segemented result (in read_single.py):

![alt text](https://github.com/eagle13gy/dicom_contour/blob/master/figures/thresholding_single.png)

In this one data set, the performance is rather good. 

### statistical_analysis.py:
Use the above method to segment the entire data set, visualize a few data set with comparision to manual segmentation, and show some results with different threshold selections:

![alt text](https://github.com/eagle13gy/dicom_contour/blob/master/figures/Thres1.0.png)

![alt text](https://github.com/eagle13gy/dicom_contour/blob/master/figures/Thres0.7.png)

The simple thresholding method performs well for certain cases, but not so well for a few cases with blurred boundaries. The threshold can affect the performance, but this parameter needs manual tuning. 

Also the total number of wrongly segmented points, and the percentage of these points w.r.t manual inner contours were calcualted to statistically evaluate the performance of this method. Below is some results for a range of threshold values:

|Thres |Total   |Percentage|
| -----|:------:| --------:|
|0.4   | 30026  | 0.484595|
|0.5   | 20855  | 0.336582|
|0.6   | 17984  | 0.290247|
|0.7   | 17891  | 0.288746|
|0.8   | 20316  | 0.327883|
|0.9   | 28763  | 0.464211|
|1.0   | 46058  | 0.743338|


| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |


### Questions:
#### Did you change anything from the pipelines built in Parts 1 to better streamline the pipeline built in Part 2? If so, what? If not, is there anything that you can imagine changing in the future?

Originally I have the third dimension to stack the data, I changed this dimension to the first one to easily extract a batch of data, and also to be consistent with most DL toolbox.

#### How do you/did you verify that the pipeline was working correctly?

I visualize a few batches to see if they're randomly selected, and covered the whole data set. 
During the debugging period, I also output some class variables (e.g. start, end, _epochs_completed, _index_in_epoch) to check how the indices are chosen for a few epoches. 

#### Given the pipeline you have built, can you see any deficiencies that you would change if you had more time? If not, can you think of any improvements/enhancements to the pipeline that you could build in?

1. One thing is how to handle if the total sample number is not a multiple of batch_size. I think there're multple ways to handle this. 
The next_batch implementation just loop into the next epoch to fill the batch_size. One easy implementation is to just discard the last few samples that couldn't fill a whole batch.
2. There're also multiple ways to implement this pipeline. I also showed that in Keras, model.fit function can easily shuffle the samples by setting a flag. 
Another easy way to implement this is to come up with an array of randomly shuffled indices of (1:num_sample) for each epoch, 
and sequentially take batch_size of the indices to sample the numpy arrays of dicoms and contours. This can be implemented without class, in the training process.
3. I think the way I stacked the numpy arrays may not be safe, a better way should be to use the list, starting with an empty list. 
However, this requires converting the list into numpy arrays in the later implementaions.


