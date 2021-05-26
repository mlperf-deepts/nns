# (c) Copyright [2017] Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import typing
import tensorflow as tf
from nns.model import Model
# InputLayer layer for sequential models, Input layer for functional API.
from tensorflow.keras.layers import (InputLayer, Input, Conv2D, BatchNormalization, Activation, Dense, Dropout,
                                     MaxPooling2D, AveragePooling2D, Add, Flatten, Layer)


"""
Most models from Deep Learning Benchmarking Suite:
    https://hewlettpackard.github.io/dlcookbook-dlbs/#/models/models?id=models
"""

__ALL__ = ['EnglishAcousticModel', 'AlexNet', 'DeepMNIST', 'VGG', 'Overfeat', 'ResNet']


Kernel2D = typing.Union[int, typing.Tuple, typing.List]
Strides2D = typing.Union[int, typing.Tuple, typing.List]


class EnglishAcousticModel(Model):
    """ https://ethereon.github.io/netscope/#/gist/10f5dee56b6f7bbb5da26749bd37ae16 """
    def __init__(self) -> None:
        super().__init__('EnglishAcousticModel')

    def create(self) -> tf.keras.models.Model:
        return tf.keras.models.Sequential([
            InputLayer((540,), name='input'),
            Dense(2048, activation='relu', name='dense1'),
            Dense(2048, activation='relu', name='dense2'),
            Dense(2048, activation='relu', name='dense3'),
            Dense(2048, activation='relu', name='dense4'),
            Dense(2048, activation='relu', name='dense5'),
            Dense(8192, activation='softmax', name='dense6')
        ], name=self.name)


class AlexNet(Model):
    """
        AlexNet:    https://ethereon.github.io/netscope/#/gist/5c94a074f4e4ac4b81ee28a796e04b5d
        AlexNetOWT: https://ethereon.github.io/netscope/#/gist/dc85cc15d59d720c8a18c4776abc9fd5
    """
    def __init__(self, version: typing.Optional[str] = None) -> None:
        super().__init__('AlexNetOWT' if version == 'owt' else 'AlexNet')
        self.filters = [64, 192, 384, 256, 256] if version == 'owt' else [96, 256, 384, 384, 256]

    def create(self) -> tf.keras.models.Model:
        return tf.keras.models.Sequential([
            InputLayer((227, 227, 3), name='input'),
            Conv2D(self.filters[0], (11, 11), strides=(4, 4), padding='valid', activation='relu', name='conv1'),
            MaxPooling2D((3, 3), strides=(2, 2)),
            Conv2D(self.filters[1], (5, 5), padding='same', activation='relu', name='conv2'),
            MaxPooling2D((3, 3), strides=(2, 2)),
            Conv2D(self.filters[2], (3, 3), padding='same', activation='relu', name='conv3'),
            Conv2D(self.filters[3], (3, 3), padding='same', activation='relu', name='conv4'),
            Conv2D(self.filters[4], (3, 3), padding='same', activation='relu', name='conv5'),
            MaxPooling2D((3, 3), strides=(2, 2)),
            Flatten(),
            Dense(4096, activation='relu', name='fc6'),
            Dropout(0.5),
            Dense(4096, activation='relu', name='fc7'),
            Dropout(0.5),
            Dense(1000, activation='softmax', name='fc8')
        ], name=self.name)


class DeepMNIST(Model):
    """ https://ethereon.github.io/netscope/#/gist/9c75cd95891207082bd42264eb7a2706 """
    def __init__(self) -> None:
        super().__init__('DeepMNIST')

    def create(self) -> tf.keras.models.Model:
        return tf.keras.models.Sequential([
            InputLayer((28, 28, 1), name='input'),
            Flatten(),
            Dense(2500, activation='relu', name='dense1'),
            Dense(2000, activation='relu', name='dense2'),
            Dense(1500, activation='relu', name='dense3'),
            Dense(1000, activation='relu', name='dense4'),
            Dense(500, activation='relu', name='dense5'),
            Dense(10, activation='softmax', name='dense6')
        ], name=self.name)


class VGG(Model):
    """
        VGG11: https://ethereon.github.io/netscope/#/gist/5550b93fb51ab63d520af5be555d691f
        VGG13: https://ethereon.github.io/netscope/#/gist/a96ba317064a61b22a1742bd05c54816
        VGG16: https://ethereon.github.io/netscope/#/gist/050efcbb3f041bfc2a392381d0aac671
        VGG19: https://ethereon.github.io/netscope/#/gist/f9e55d5947ac0043973b32b7ff51b778
    """
    CONFIGS = {
        'vgg11': {'name': 'VGG11', 'specs': ([1, 1, 2, 2, 2], [64, 128, 256, 512, 512])},
        'vgg13': {'name': 'VGG13', 'specs': ([2, 2, 2, 2, 2], [64, 128, 256, 512, 512])},
        'vgg16': {'name': 'VGG16', 'specs': ([2, 2, 3, 3, 3], [64, 128, 256, 512, 512])},
        'vgg19': {'name': 'VGG19', 'specs': ([2, 2, 4, 4, 4], [64, 128, 256, 512, 512])}
    }

    def __init__(self, version: str = 'vgg11') -> None:
        super().__init__(VGG.CONFIGS[version]['name'])
        self.version = version

    def create(self) -> tf.keras.models.Model:
        layers, filters = VGG.CONFIGS[self.version]['specs']
        model = tf.keras.models.Sequential([InputLayer((224, 224, 3), name='input')], name=self.name)
        for i, num in enumerate(layers):
            for j in range(num):
                model.add(Conv2D(filters[i], (3, 3), padding='same', activation='relu',
                                 name='conv{}_{}'.format(i+1, j+1)))
            model.add(MaxPooling2D((2, 2), strides=(2, 2), name='pool{}'.format(i+1)))
        model.add(Flatten())
        for i in range(2):
            model.add(Dense(4096, activation='relu', name='fc{}'.format(6+i)))
            model.add(Dropout(0.5, name='dropout{}'.format(6+i)))
        model.add(Dense(1000, activation='softmax', name='fc8'))
        return model


class Overfeat(Model):
    """ https://ethereon.github.io/netscope/#/gist/ebfeff824393bcd66a9ceb851d8e5bde """
    def __init__(self) -> None:
        super().__init__('Overfeat')

    def create(self) -> tf.keras.models.Model:
        return tf.keras.models.Sequential([
            InputLayer((231, 231, 3), name='input'),
            Conv2D(96, (11, 11), strides=(4, 4), padding='valid', activation='relu', name='conv1'),
            MaxPooling2D((2, 2), strides=(2, 2)),
            Conv2D(256, (5, 5), padding='valid', activation='relu', name='conv2'),
            MaxPooling2D((2, 2), strides=(2, 2)),
            Conv2D(512, (3, 3), padding='same', activation='relu', name='conv3'),
            Conv2D(1024, (3, 3), padding='same', activation='relu', name='conv4'),
            Conv2D(1024, (3, 3), padding='same', activation='relu', name='conv5'),
            MaxPooling2D((2, 2), strides=(2, 2)),
            Flatten(),
            Dense(3072, activation='relu', name='fc6'),
            Dropout(0.5),
            Dense(4096, activation='relu', name='fc7'),
            Dropout(0.5),
            Dense(1000, activation='softmax', name='fc8')
        ], name=self.name)


class ResNet(Model):
    """
        ResNet18:   https://ethereon.github.io/netscope/#/gist/649e0fb6c96c60c9f0abaa339da3cd27
        ResNet34:   https://ethereon.github.io/netscope/#/gist/277a9604370076d8eed03e9e44e23d53
        ResNet50:   https://ethereon.github.io/netscope/#/gist/db945b393d40bfa26006
        ResNet101:  https://ethereon.github.io/netscope/#/gist/b21e2aae116dc1ac7b50
        ResNet152:  https://ethereon.github.io/netscope/#/gist/d38f3e6091952b45198b
        ResNet200:  https://ethereon.github.io/netscope/#/gist/38a20d8dd1a4725d12659c8e313ab2c7
        ResNet269:  https://ethereon.github.io/netscope/#/gist/fbf7c67565523a9ac2c349aa89c5e78d
    """
    CONFIGS = {
        'resnet18': {'name': 'ResNet18', 'units': [2, 2, 2, 2], 'num_layers': 18},
        'resnet34': {'name': 'ResNet34', 'units': [3, 4, 6, 3], 'num_layers': 34},
        'resnet50': {'name': 'ResNet50', 'units': [3, 4, 6, 3], 'num_layers': 50},
        'resnet101': {'name': 'ResNet101', 'units': [3, 4, 23, 3], 'num_layers': 101},
        'resnet152': {'name': 'ResNet152', 'units': [3, 8, 36, 3], 'num_layers': 152},
        'resnet200': {'name': 'ResNet200', 'units': [3, 24, 36, 3], 'num_layers': 200},
        'resnet269': {'name': 'ResNet269', 'units': [3, 30, 48, 8], 'num_layers': 269}
    }

    def __init__(self, version: str = 'resnet50') -> None:
        super().__init__(ResNet.CONFIGS[version]['name'])
        self.version = version
        if ResNet.CONFIGS[version]['num_layers'] >= 50:
            self.filter_list = [64, 256, 512, 1024, 2048]
            self.bottle_neck = True
        else:
            self.filter_list = [64, 64, 128, 256, 512]
            self.bottle_neck = False

    @staticmethod
    def conv_block(input_: Layer, num_filters: int, kernel: Kernel2D, strides: Strides2D = (1, 1),
                   padding: str = 'valid', activation: typing.Optional[str] = 'relu',
                   name: typing.Optional[str] = None) -> Layer:
        x = Conv2D(num_filters, kernel, strides=strides, padding=padding, activation=None,
                   use_bias=False, name=name + '/conv')(input_)
        x = BatchNormalization(name=name + '/bn')(x)
        if activation is not None:
            x = Activation(activation=activation, name=name + '/' + activation)(x)
        return x

    @staticmethod
    def residual_unit(input_: Layer, num_filters: int, stride: Strides2D, dim_match: bool, is_bottleneck: bool,
                      name: str) -> Layer:
        # Branch 1
        shortcut = input_ if dim_match else ResNet.conv_block(input_, num_filters, (1, 1), stride, 'same', None,
                                                              name=name + '/branch1')
        # Branch 2
        if is_bottleneck:
            x = ResNet.conv_block(input_, num_filters // 4, (1, 1), name=name + '/branch2a')              # Block 2A
            x = ResNet.conv_block(x, num_filters // 4, (3, 3), stride, 'same', name=name + '/branch2b')   # Block 2B
            x = ResNet.conv_block(x, num_filters, (1, 1), activation=None, name=name + '/branch2c')       # Block 2C
        else:
            x = ResNet.conv_block(input_, num_filters, (3, 3), stride, 'same', name=name + '/branch2a')   # Block 2A
            x = ResNet.conv_block(x, num_filters, (3, 3), (1, 1), 'same', None, name=name + '/branch2b')  # Block 2B
        # Final aggregation
        x = Add(name=name + '/sum')([shortcut, x])
        x = Activation(activation='relu', name=name + '/relu')(x)
        return x

    def create(self) -> tf.keras.models.Model:
        units = self.CONFIGS[self.version]['units']
        input_ = Input((224, 224, 3), name='input')
        x = ResNet.conv_block(input_, self.filter_list[0], (7, 7), (2, 2), 'same', name='conv1')
        x = MaxPooling2D((3, 3), strides=(2, 2), padding='same', name='conv1/mpool')(x)

        for i in range(len(units)):
            x = ResNet.residual_unit(x, self.filter_list[i + 1], (1 if i == 0 else 2), False, self.bottle_neck,
                                     name='res{}a'.format(i + 1))
            for j in range(units[i] - 1):
                x = ResNet.residual_unit(x, self.filter_list[i + 1], 1, True, self.bottle_neck,
                                         name='res{}b{}'.format(i + 1, j + 1))

        x = AveragePooling2D((7, 7), name='apool')(x)
        x = Flatten(name='flatten')(x)
        x = Dense(1000, activation='softmax', name='output')(x)

        return tf.keras.models.Model(input_, x, name=self.name)
