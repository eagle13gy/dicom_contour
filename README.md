Pipeline to read paired Dicom and Contours
============================================================
Yi Guo


Part 1
--------------
### read_single.py: 
Unit test to read one dicom/contour file to verify if the read functions are working properly.
Plot the dicom and corresponding contour after successful read to check if the ROI is reasonable:

![alt text](https://github.com/eagle13gy/dicom_contour/blob/master/single_res.png)

### link_data.py:
**parsing_data(filedir)**:
Parse the given DICOM files and contour files using the linked CVS.
Return 2 numpy arrays, 1 containing all the dicoms, and the other containing all the contour masks. 
The first dimension is used to concantenate the images/masks.


**visulize_dicom_contour(dicoms,contours,Nrow,Ncol)** : 
A small utility to visulize first few paired dicoms and contours using subplots

![alt text](https://github.com/eagle13gy/dicom_contour/blob/master/multi_res.png)

### Questions:
#### How did you verify that you are parsing the contours correctly?
I plotted the dicom images and overlaped the contour onto the images, and showed them side by side to check if the read function works correctly and the contours are reasonable.

#### What changes did you make to the code, if any, in order to integrate it into our production code base? 
Although all the images given are of the same width and heighth (256*256), 
the function poly_to_mask(polygon, width, height) has width comes before height, which seems inconsistent with the numpy.shape. 
I've changed this module to have height comes before width. 

Part 2
--------------
### batch_test.py: 
Define a class (Dataset) which has a method next_batch(batch_size, shuffle), with shuffle default to be true. 
This module is adapted from the mnist data processing in tensorflow toolbox. 
This next_batch method will return a single batch with random samples over the entire data set. 

To test it, plot a few batches of images and contours using the visulize_dicom_contour function. 
Showing here is one batch of random samples. 

![alt text](https://github.com/eagle13gy/dicom_contour/blob/master/batch_res.png)

### cnn_train_keras.py:
Train on a pseudo CNN with output size same as input size. 
Use parsing_data to load the dicom and boolen mask here, random shuffle can be enabled by Keras model.fit

**visulize_dicom_contour(dicoms,contours,Nrow,Ncol)** : 
A small utility to visulize first few paired dicoms and contours using subplots


### Questions:
#### How did you verify that you are parsing the contours correctly?
I plotted the dicom images and overlaped the contour onto the images, and showed them side by side to check if the read function works correctly and the contours are reasonable.

#### What changes did you make to the code, if any, in order to integrate it into our production code base? 



