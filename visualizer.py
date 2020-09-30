import numpy as np

from keras import models
from keras import layers

import matplotlib.pyplot as plt


# visualize the first 32 conv-filter in the set-recognition-net
# by creating subplots
def visualizeLayerKernels(layer):
    plt.figure(figsize=(10,10))
    for i in range(32):
        plt.subplot(6,6,i+1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(layer[i], cmap='gray')
        plt.xlabel('Conv-Filter : #'+str(i+1))
    plt.show()

# reconstruct the way layers save the filter values.
# passing the data to the visualize function
if __name__ == '__main__':
    try:
        SetDetectionModel = models.load_model('SetDetectionModel')
        layer1 = SetDetectionModel.layers[0]
        kernels = layer1.get_weights()[0].reshape([32,3,3,1]) 
        visualizeLayerKernels(kernels)
    except Exception as e:
        print(e)