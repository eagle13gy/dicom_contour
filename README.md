Pipeline to read paired dicoms and contours
============================================================
Yi Guo


Part 1
--------------
### read_single.py: 
Unit test to read one dicom/contour file to verify if the read functions are working properly.
Plot the dicom and the corresponding contour after successful read to check if the ROI is reasonable:

![alt text](https://github.com/eagle13gy/dicom_contour/blob/master/single_res.png)

### link_data.py:
**parsing_data(filedir)**:
Parse the given DICOM files and contour files using the linked CVS.
Return 2 numpy arrays, 1 containing all the dicoms, and the other containing all the contour masks. 
The first dimension is used to concantenate the images/masks.


**visualize_dicom_contour(dicoms,contours,Nrow,Ncol)** : 
A small utility to visualize first few paired dicoms and contours using subplots

![alt text](https://github.com/eagle13gy/dicom_contour/blob/master/multi_res.png)

### Questions:
#### How did you verify that you are parsing the contours correctly?
I plotted the dicom images and overlaped the contour onto the images, and showed them side by side to check if the read function works correctly and the contours are reasonable.

#### What changes did you make to the code, if any, in order to integrate it into our production code base? 
Although all the images given are of the same width and height (256*256), 
the function poly_to_mask(polygon, width, height) has width comes before height, which seems inconsistent with the numpy.shape. 
I've changed this module to have height come before width. 

Part 2
--------------
### batch_test.py: 
Define a class (Dataset) which has a method next_batch(batch_size, shuffle), with shuffle default to be true. 
This module is adapted from the mnist data processing part in tensorflow toolbox. 
This next_batch method will return a single batch with random samples over the entire data set, and will cycle over the entire data set during one epoch.

To test it, plot a few batches of images and contours using the visualize_dicom_contour function. 
Showing here is one batch of random samples. 

![alt text](https://github.com/eagle13gy/dicom_contour/blob/master/batch_res.png)

### cnn_train_keras.py:
Train on a dummy CNN (one conv, one deconv layer) with output size same as input size. 
Use parsing_data to load the dicoms and contours here, random shuffle can be enabled by Keras model.fit


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


