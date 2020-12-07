import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models

#https://www.kaggle.com/datamunge/sign-language-mnist
#hand gesture recog with CNN
f=open('sign_mnist_train.csv')
f.readline()
data=[]
ans=[]
count=0
for n,x in enumerate(f):
    line=x.split(',')
    ans.append(int(line.pop(0)))
    temp=np.array(line)
    temp=temp.astype(float)
    temp=temp.reshape(28,28,1)
    data.append(temp)
train=np.array(data)
train/=255.0
train=train.reshape(len(train),28,28,1)
trainLabels=np.array(ans)

f=open('sign_mnist_test.csv')
f.readline()
data=[]
ans=[]
count=0
for n,x in enumerate(f):
    line=x.split(',')
    ans.append(int(line.pop(0)))
    temp=np.array(line)
    temp=temp.astype(float)
    temp=temp.reshape(28,28,1)
    data.append(temp)
test=np.array(data)
test/=255.0
test=test.reshape(len(test),28,28,1)
testLabels=np.array(ans)
class_names = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28,1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (2, 2), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (2, 2), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(26))

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
history = model.fit(train, trainLabels, epochs=20,
                    validation_data=(test, testLabels))

cap=cv2.VideoCapture(0)
while True:
    s,temp=cap.read()
    bbLC=(0,0)
    bbRC=(300,300)
    rob=temp[bbLC[0]:bbRC[0], bbLC[1]:bbRC[1]]
    cv2.rectangle(temp,bbLC,bbRC,(0,255,0),0)
    cv2.imshow("test", temp)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break
    temp = cv2.cvtColor(rob,cv2.COLOR_BGR2GRAY)
    temp = cv2.bitwise_not(temp)
    resized = cv2.resize(temp, (28,28), interpolation = cv2.INTER_AREA)
    #print(type(resized))
    cv2.imshow("Resized image", resized)
    resized=np.array(resized)
    resized=resized.astype(float)
    resized/=255.0
    resized=np.array([resized])
    resized=resized.reshape(1,28,28,1)
    print(class_names[model.predict_classes(resized)[0]])
