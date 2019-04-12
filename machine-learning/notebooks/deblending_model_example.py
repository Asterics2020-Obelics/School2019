from keras.models import Sequential, Model
from keras.layers import (
    Conv2D,
    Dropout,
    Input,
    MaxPooling2D,
    concatenate,
    Conv2DTranspose,
    UpSampling2D,
)
from keras.layers.noise import GaussianNoise


def model():
    input_shape = (128, 128, 1)
    output_channels = 1
    depth = 16
    n_layers = 6
    conv_size0 = (3, 3)
    conv_size = (3, 3)
    last_conv_size = (3, 3)
    activation = "relu"
    last_activation = "sigmoid"
    dropout_rate = 0
    sigma_noise = 0.01
    initialization = "he_normal"

    model = Sequential()
    model.add(
        Conv2D(
            depth,
            conv_size0,
            input_shape=input_shape,
            activation=activation,
            padding="same",
            name="conv0",
            kernel_initializer=initialization,
        )
    )
    if dropout_rate > 0:
        model.add(Dropout(dropout_rate))

    for layer_n in range(1, n_layers):
        model.add(
            Conv2D(
                depth,
                conv_size,
                activation=activation,
                padding="same",
                name="conv{}".format(layer_n),
                kernel_initializer=initialization,
            )
        )
        if dropout_rate > 0:
            model.add(Dropout(dropout_rate))

    if sigma_noise > 0:
        model.add(GaussianNoise(sigma_noise))

    model.add(
        Conv2D(
            output_channels,
            last_conv_size,
            activation=last_activation,
            padding="same",
            name="last",
            kernel_initializer=initialization,
        )
    )

    return model
