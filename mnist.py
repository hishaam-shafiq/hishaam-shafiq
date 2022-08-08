import numpy as np
np.set_printoptions(suppress=True)
import matplotlib.pyplot as plt

from tensorflow import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils

(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# mnist = np.load('data/MNIST/mnist.npz')
# train_images = mnist['train_images']
# train_labels = mnist['train_labels']
# test_images = mnist['test_images']
# test_labels = mnist['test_labels']

# plot some random images from training data
size = (10,3)    # plot 10x3 images
fig, ax = plt.subplots(size[1], size[0], figsize=size)
ax = ax.flatten()
for i in range(np.prod(size)):
    r = np.random.randint(train_images.shape[0])    # pick a random image
    ax[i].imshow(train_images[r], cmap='Greys')    # plot image
    ax[i].axis('off')
plt.show()

# convert data to appropriate form
X_train = train_images.reshape(-1, 28, 28, 1) / 255
X_test = test_images.reshape(-1, 28, 28, 1) / 255
Y_train = np_utils.to_categorical(train_labels, 10)
Y_test = np_utils.to_categorical(test_labels, 10)

# define model architecture
model = Sequential()
model.add(Convolution2D(filters=16, kernel_size=8, strides=2, activation='relu', input_shape=(28,28,1)))
model.add(Convolution2D(filters=8, kernel_size=5, strides=2, activation='relu'))
# model.add(MaxPooling2D(pool_size=(2,2)))
# model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(32, activation='relu'))
# model.add(Dropout(0.5))
model.add(Dense(10, activation='softmax'))

# compile model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# print model information
model.summary()

# fit model on training data
model.fit(X_train, Y_train, batch_size=100, epochs=10, verbose=1)

# evaluate model on testing data
model.evaluate(X_test, Y_test, verbose=1)

# load and show new drawing
drawing = plt.imread('figures/7times.png')
plt.figure(figsize=(1,1))
plt.imshow(drawing, vmin=0, vmax=1, cmap='Greys')
plt.axis('off')
plt.show()

# predict class of new drawing
drawing = drawing.reshape((-1,28,28,1))
output = model.predict(drawing)
print(output)

digit = np.argmax(output, axis=1)
print(digit[0])
