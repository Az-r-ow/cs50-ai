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

For my second take, I increased the Max pooling pool size to `3 x 3`. And decreased the hidden layer's nodes to `64`.
However the results has not improved the slightest, in the contrary, the accuracy decreased by `0.0051`.

For the third take, I decided to add another convolution step. The parameters for the initial one were :
- `64` filters
- `3 x 3 ` kernel size
- `3 x 3` MaxPooling pool size

The second convolution had :
- `32` filters
- `3 x 3` kernel size
- `3 x 3` Pool size

In addition, I added two extra hidden layers one of them with a dropout of `0.2`. And changed the previously added hidden layer's dropout to `0.2` as well.

With these layers this is how our Neural Network performed :
```
Epoch 1/10
500/500 [==============================] - 4s 8ms/step - loss: 3.4260 - accuracy: 0.1296
Epoch 2/10
500/500 [==============================] - 4s 8ms/step - loss: 2.2432 - accuracy: 0.3452
Epoch 3/10
500/500 [==============================] - 4s 8ms/step - loss: 1.8181 - accuracy: 0.4228
Epoch 4/10
500/500 [==============================] - 4s 8ms/step - loss: 1.5802 - accuracy: 0.4966
Epoch 5/10
500/500 [==============================] - 4s 8ms/step - loss: 1.3426 - accuracy: 0.5674
Epoch 6/10
500/500 [==============================] - 4s 8ms/step - loss: 1.1356 - accuracy: 0.6321
Epoch 7/10
500/500 [==============================] - 4s 8ms/step - loss: 0.9701 - accuracy: 0.6775
Epoch 8/10
500/500 [==============================] - 4s 8ms/step - loss: 0.8603 - accuracy: 0.7050
Epoch 9/10
500/500 [==============================] - 4s 8ms/step - loss: 0.8046 - accuracy: 0.7329
Epoch 10/10
500/500 [==============================] - 4s 8ms/step - loss: 0.7112 - accuracy: 0.7640
333/333 - 1s - loss: 0.5386 - accuracy: 0.8224 - 1s/epoch - 3ms/step
```

A great improvement from my initial take. However, more is needed to achive the 95% accuracy and higher.

Reading the following [article](https://pyimagesearch.com/2018/12/31/keras-conv2d-and-convolutional-layers/) on the importance of the `keras.layers.Conv2D` parameters. The author recommended to start with a lower number of layers for the first Convolution and then going up if needed. So instead of starting with `64` layers and then `34` I started with `32` and then went for `64`. And also I rectified my second max pooling to a `(2 x 2)` pool size. These were the results after these changes :

```
Epoch 1/10
500/500 [==============================] - 4s 7ms/step - loss: 3.5033 - accuracy: 0.1351   
Epoch 2/10
500/500 [==============================] - 4s 7ms/step - loss: 2.0187 - accuracy: 0.3967
Epoch 3/10
500/500 [==============================] - 4s 7ms/step - loss: 1.4337 - accuracy: 0.5243
Epoch 4/10
500/500 [==============================] - 4s 7ms/step - loss: 1.1122 - accuracy: 0.6249
Epoch 5/10
500/500 [==============================] - 4s 7ms/step - loss: 0.8552 - accuracy: 0.7082
Epoch 6/10
500/500 [==============================] - 4s 7ms/step - loss: 0.6860 - accuracy: 0.7650
Epoch 7/10
500/500 [==============================] - 4s 7ms/step - loss: 0.5665 - accuracy: 0.8081
Epoch 8/10
500/500 [==============================] - 4s 7ms/step - loss: 0.5192 - accuracy: 0.8323
Epoch 9/10
500/500 [==============================] - 4s 7ms/step - loss: 0.4531 - accuracy: 0.8503
Epoch 10/10
500/500 [==============================] - 4s 7ms/step - loss: 0.3931 - accuracy: 0.8719
333/333 - 1s - loss: 0.2605 - accuracy: 0.9289 - 916ms/epoch - 3ms/step
```

**Closer than ever !**
