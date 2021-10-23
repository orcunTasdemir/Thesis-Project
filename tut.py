# Create your first MLP in Keras
from keras.models import Sequential
from keras.layers import Dense
import numpy
from tensorflow.python.framework.ops import init_scope
# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)
# load pima indians dataset
dataset = numpy.loadtxt("dataSet.csv", delimiter=",")
# split into input (X) and output (Y) variables
#every row from 0th to the 7th item
X = dataset[:,0:8]
print(X.shape)
#means all the rows and the 8th item in every row
Y = dataset[:,8]
print(Y.shape)
# # create model
# model = Sequential()
# model.add(Dense(12, input_dim=8, activation='relu'))
# model.add(Dense(8, activation='relu'))
# model.add(Dense(1, activation='sigmoid'))
# # Compile model
# model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# # Fit the model
# model.fit(X, Y, validation_split=0.33, epochs=150, batch_size=10)
# # evaluate the model
# scores = model.evaluate(X, Y)
# print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
# # for me I got acc: 76.69%