import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import argparse as arg

from itertools import cycle
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator

parser = arg.ArgumentParser()
parser.add_argument("TRAIN")
parser.add_argument("VALID")
parser.add_argument("TEST")
args = parser.parse_args()

# Каталог с нашими обучающими фотографиями собак
train_dogs_dir = os.path.join(args.TRAIN+'/dogs')
# Каталог с фотографиями людей
train_people_dir = os.path.join(args.TRAIN+'/people')
# Каталог с нашими проверенными фотографиями собак
valid_dogs_dir = os.path.join(args.VALID+'/dogs')
# Каталог с нашими проверенными фотографиями людей
valid_people_dir = os.path.join(args.VALID +'/people')

train_dogs_names = os.listdir(train_dogs_dir)
train_people_names = os.listdir(train_people_dir)
validation_dogs_names = os.listdir(valid_dogs_dir)
validation_people_names = os.listdir(valid_people_dir)

# Выводится общее количество изображений каталогах
print('total training dogs images:', len(os.listdir(train_dogs_dir)))
print('total training people images:', len(os.listdir(train_people_dir)))
print('total validation dogs images:', len(os.listdir(valid_dogs_dir)))
print('total validation people images:', len(os.listdir(valid_people_dir)))

# Все изображения будут масштабированы на 1./255
train_datagen = ImageDataGenerator(rescale=1/255)
validation_datagen = ImageDataGenerator(rescale=1/255)

train_generator = train_datagen.flow_from_directory(
        args.TRAIN, 
        classes = ['dogs', 'people'],
        target_size=(200, 200),
        batch_size=402,
        class_mode='binary')

validation_generator = validation_datagen.flow_from_directory(
        args.VALID, 
        classes = ['dogs', 'people'],
        target_size=(200, 200),
        batch_size=39,
        class_mode='binary',
        shuffle=False)

# Cоздается модель нейронной сети с использованием библиотеки TensorFlow и Keras.
model = tf.keras.models.Sequential([tf.keras.layers.Flatten(input_shape = (200,200,3)),
                                    tf.keras.layers.Dense(128, activation=tf.nn.relu),
                                    tf.keras.layers.Dense(1, activation=tf.nn.sigmoid)])

model.summary() # выводит сводную информацию о NN

# В данном участке кода компилируется модель нейронной сети после ее создания и определения слоев
# Компиляция модели включает определение оптимизатора, функции потерь и метрик для оценки производительности модели во время обучения.
model.compile(optimizer = tf.keras.optimizers.Adam(),
              loss = 'binary_crossentropy',
              metrics=['accuracy'])

#  Обучение модели нейронной сети с использованием метода fit()
history = model.fit(
      train_generator,
      epochs=8,
      verbose=1,
      validation_data=validation_generator)


# список используется для указания имени файла изображения,
# которое будет загружено и классифицировано моделью
uploaded = sorted(name for name in os.listdir(args.TEST)
                  if name.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))
                  and os.path.isfile(os.path.join(args.TEST, name)))

for fn in uploaded:
    path = os.path.join(args.TEST, fn)
    img = image.load_img(path, target_size=(200, 200)) #для загрузки изображения с указанным путем и изменением его размера
    x = image.img_to_array(img) # для преобразования загруженного изображения в числовой массив
    plt.imshow(x/255.) #  для отображения изображения, представленного в массиве x, с применением нормализации значений пикселей
    x = np.expand_dims(x / 255.0, axis=0) # для расширения размерности массива
    images = np.vstack([x]) # для вертикальной стыковки массивов
    classes = model.predict(images, batch_size=10) #для получения прогнозируемых классов или вероятностей классов для входных данных

    print(classes[0])
    if classes[0] < 0.5:
        print(fn + " is a dog")
    else:
        print(fn + " is a human")
