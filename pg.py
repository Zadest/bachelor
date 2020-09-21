from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
#
import numpy as np
import os
import platform
#
import random
#
from config import classes
from PIL import Image
import requests

# config part
if platform.system() == 'Windows':
    _filePath = 'E:\\Python\\Bachelor\\'
else:
    _filePath = '~/Python/Bachelor/'

################################
#                              #
# Example by Francois Chollet  #
#                              #
################################
'''datagen = ImageDataGenerator(
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=False,
        fill_mode='nearest')

img = Image.open(_filePath+'Data\\train\\m21\\m21-1.jpg')
x =  np.array(img)
x = x.reshape((1,)+x.shape)

i = 0
for batch in datagen.flow(x,batch_size=1,save_to_dir=_filePath+'preview',save_prefix='m21',save_format='jpeg'):
    i += 1
    if i > 20:
        break
'''        
## model

model = Sequential()
model.add(Conv2D(32,(3,3),activation='relu',input_shape=(204,146,3)))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(32,(3,3),activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(64,(3,3),activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Flatten())
model.add(Dense(64,activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(8))

model.summary()
model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])


batch_size = 1

train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=False
)

test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
        _filePath+'data\\train',
        target_size=(204,146),
        batch_size=batch_size)
        
validation_generator = train_datagen.flow_from_directory(
        _filePath+'data\\validation',
        target_size=(204,146),
        batch_size=batch_size)

history = model.fit(train_generator,epochs = 50,validation_data=validation_generator)

model.save_weights('first_try.h5')
##############################


#
if __name__ == '__main__':
    if not os.path.exists('E:\\Python\\Bachelor\\Data'):
        os.mkdir('E:\\Python\\Bachelor\\Data')
    if not os.path.exists('E:\\Python\\Bachelor\\Data\\train'):
        os.mkdir('E:\\Python\\Bachelor\\Data\\train')
    if not os.path.exists('E:\\Python\\Bachelor\\Data\\validation'):
        os.mkdir('E:\\Python\\Bachelor\\Data\\validation')
    
    for name in classes.values():
        if not os.path.exists('E:\\Python\\Bachelor\\Data\\train\\'+name):
            os.mkdir('E:\\Python\\Bachelor\\Data\\train\\'+name)
        if not os.path.exists('E:\\Python\\Bachelor\\Data\\validation\\'+name):
            os.mkdir('E:\\Python\\Bachelor\\Data\\validation\\'+name)
        
    files = os.listdir(_filePath+'1\\')
    for f in files:
        if 'jpg' in f and f.split('-')[0] in classes.values():
            folder = f.split('-')[0]
            if random.randint(0,3) < 3:
                Image.open(_filePath+'1\\'+f).save(_filePath+'Data\\train\\'+folder+'\\'+f)
            else:
                Image.open(_filePath+'1\\'+f).save(_filePath+'Data\\validation\\'+folder+'\\'+f)