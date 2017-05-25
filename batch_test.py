from utilities import *

"""A DataSet class with next_Batch method
Initialize with the file directory as parameter
next_batch will return one numpy array for images (dicom) and one numpy array for targets(contour)
By default, a batch will get samples randomly from the entire data set during one epoch
"""

class DataSet(object):
    def __init__(self, filedir):
        dicoms, contours = parsing_data(filedir)
        self._images = dicoms
        self._labels = contours
        self._epochs_completed = 0
        self._index_in_epoch = 0
        self._num_examples=dicoms.shape[0]

    def next_batch(self, batch_size, shuffle=True):
        start = self._index_in_epoch
        # Shuffle the indices for the first epoch
        if self._epochs_completed == 0 and start == 0 and shuffle:
            perm0 = np.arange(self._num_examples)
            np.random.shuffle(perm0)
            self._images = self._images[perm0]
            self._labels = self._labels[perm0]

        # Go to the next epoch
        if start + batch_size > self._num_examples:
            # Finished epoch
            self._epochs_completed += 1
            # Get the rest examples in this epoch
            rest_num_examples = self._num_examples - start
            images_rest_part = self._images[start:self._num_examples]
            labels_rest_part = self._labels[start:self._num_examples]
            # Shuffle the data
            if shuffle:
                perm = np.arange(self._num_examples)
                np.random.shuffle(perm)
                self._images = self._images[perm]
                self._labels = self._labels[perm]
            # Start next epoch
            start = 0
            self._index_in_epoch = batch_size - rest_num_examples
            end = self._index_in_epoch
            images_new_part = self._images[start:end]
            labels_new_part = self._labels[start:end]
            return np.concatenate((images_rest_part, images_new_part), axis=0), np.concatenate(
                (labels_rest_part, labels_new_part), axis=0)
        else:
            self._index_in_epoch += batch_size
            end = self._index_in_epoch
            return self._images[start:end], self._labels[start:end]

# test a few batches by visualizing the images and corresponding contours
d1=DataSet('final_data')
for i in range(20):
    a,b=d1.next_batch(9)
#    a,b=d1.next_batch(9,False)
    plt.figure(figsize=(20,10))
    visualize_dicom_contour(a,b,2,4)

plt.show()

