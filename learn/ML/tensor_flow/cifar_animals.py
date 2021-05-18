import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt
import sys

num_classes = 10
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
print("Num CPUs Available: ", len(tf.config.list_physical_devices('CPU')))
print(tf.config.list_physical_devices())
# tf.debugging.set_log_device_placement(True)

# with tf.device('/CPU:0'):
with tf.device('/GPU:0'):

    (x_train, y_train), (x_test, y_test) = datasets.mnist.load_data()
    print(x_train.shape, x_train.shape)

    x_train = x_train.astype("float32") / 255
    x_test = x_test.astype("float32") / 255

    print("x_train shape:", x_train.shape)
    print(x_train.shape[0], "train samples")
    print(x_test.shape[0], "test samples")

    y_train = tf.keras.utils.to_categorical(y_train, num_classes)
    y_test = tf.keras.utils.to_categorical(y_test, num_classes)

    x_train = x_train.reshape((x_train.shape[0], 28, 28, 1))
    x_test = x_test.reshape((x_test.shape[0], 28, 28, 1))
    print(x_train.shape, y_train.shape)
    # sys.exit()

    input_shape = (28, 28, 1)
    model = tf.keras.Sequential()

    model.add(layers.Conv2D(4, kernel_size=(5, 5), activation="selu",
                            kernel_initializer="lecun_normal",
                            padding="same", input_shape=(28, 28, 1)))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(layers.Conv2D(8, kernel_size=(5, 5), activation="selu",
                            kernel_initializer="lecun_normal"))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(layers.Flatten())
    # model.add(layers.Dropout(0.5))
    model.add(layers.Dense(120, activation="selu", kernel_initializer="lecun_normal"))
    model.add(layers.Dense(84, activation="selu", kernel_initializer="lecun_normal"))
    model.add(layers.Dense(num_classes, activation="softmax"))

    model.summary()

    batch_size = 128
    epochs = 10

    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

history = model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1)

plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label='val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0.5, 1])
plt.legend(loc='lower right')

test_loss, test_acc = model.evaluate(x_test,  y_test, verbose=2)
print(test_acc)
plt.show()
