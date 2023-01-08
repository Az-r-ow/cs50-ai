# Traffic : Observations

I built the model by adding a convolutional 2D layer. For which I pass these arguments :
```py
 tf.keras.layers.Conv2D(64, kernel_size=(3, 3), activation='relu', input_shape=(IMG_WIDTH, IMG_HEIGHT, 3))
```
I will begin with 64 nodes and a kernel size of 3.
In addition to the convolution, I will Max pool the results and then flatten.
I will finally add a hidden layer with a 128 units and a dropout of 0.5. Following the results, I will do the necessary adjustments.
My model was able to compile with these layers but the accuracy was incredibly low :
```
Epoch 1/10
500/500 [==============================] - 4s 7ms/step - loss: 5.1708 - accuracy: 0.0524   
Epoch 2/10
500/500 [==============================] - 4s 7ms/step - loss: 3.5904 - accuracy: 0.0561
Epoch 3/10
500/500 [==============================] - 4s 8ms/step - loss: 3.5433 - accuracy: 0.0546
Epoch 4/10
500/500 [==============================] - 4s 8ms/step - loss: 3.5201 - accuracy: 0.0551
Epoch 5/10
500/500 [==============================] - 4s 8ms/step - loss: 3.5098 - accuracy: 0.0552
Epoch 6/10
500/500 [==============================] - 4s 8ms/step - loss: 3.5050 - accuracy: 0.0571
Epoch 7/10
500/500 [==============================] - 4s 8ms/step - loss: 3.5026 - accuracy: 0.0571
Epoch 8/10
500/500 [==============================] - 4s 8ms/step - loss: 3.5015 - accuracy: 0.0561
Epoch 9/10
500/500 [==============================] - 4s 8ms/step - loss: 3.5009 - accuracy: 0.0571
Epoch 10/10
500/500 [==============================] - 4s 8ms/step - loss: 3.5005 - accuracy: 0.0571
333/333 - 1s - loss: 3.4946 - accuracy: 0.0553 - 1s/epoch - 3ms/step
```


#### What did I try ?

#### What worked well ?

#### What didn't work well ?

#### What did I notice ?
