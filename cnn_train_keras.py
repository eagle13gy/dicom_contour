'''
Train on a dummy CNN with output size same as input size
Use parsing_data to load the dicom and boolen mask here
random shuffle is enabled by Keras model.fit
'''

from __future__ import print_function

from keras.models import Model
from keras.layers import Input, Conv2D, Conv2DTranspose
from utilities import *

epochs = 20

batch_size = 8
filters=1
original_dim = 256*256
img_rows, img_cols, img_chns = 256, 256, 1
original_img_size = (img_rows, img_cols, img_chns)

# read data
x_train, y_train = parsing_data('final_data')

# use first 8th as test data
x_test,y_test=x_train[:8,:,:],y_train[:8,:,:]
x_train,y_train=x_train[8:,:,:],y_train[8:,:,:]

# scale the data
x_train = x_train.astype('float32') / 500.
x_train = x_train.reshape((x_train.shape[0],) + original_img_size)
x_test = x_test.astype('float32') / 500.
x_test = x_test.reshape((x_test.shape[0],) + original_img_size)

y_train = y_train.astype('float32')
y_train = y_train.reshape((y_train.shape[0],) + original_img_size)
y_test = y_test.astype('float32')
y_test = y_test.reshape((y_test.shape[0],) + original_img_size)

print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# construct the network of 1 conv 1 deconv
x = Input(batch_shape=(batch_size,)+original_img_size)
conv_1 = Conv2D(filters,
                kernel_size=(3, 3),
                padding='same', strides=2, activation='relu')(x)

deconv_1 = Conv2DTranspose(filters,kernel_size=(3, 3),
                           padding='same',strides=2,
                           activation='relu')(conv_1)

cnn = Model(x,deconv_1)
cnn.summary()

cnn.compile(loss='mean_squared_error', optimizer='Adam')

# train with random shuffle
history = cnn.fit(x_train, y_train,
                    shuffle=True,
                    batch_size=batch_size,
                    epochs=epochs,
                    verbose=1,
                    validation_data=(x_test, y_test))

x_test_p = cnn.predict(x_test, batch_size=batch_size)

