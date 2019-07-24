import numpy as np
from keras import regularizers
from keras.models import Model
from keras.layers import Input, Conv2D, MaxPooling2D, concatenate
from IPython.display import SVG
from keras.utils.vis_utils import model_to_dot
from keras.layers import Lambda
import tensorflow as tf


def UpSampling2DBilinear(size):
    return Lambda(lambda x: tf.image.resize_bilinear(x, size, align_corners=True))


# Model names exemple: unet_3s_64-512f_r
# - unet: model name
# - 3s: 3 stages of pool/up
# - 64-512f: 64 to 512 features/filters
# - r: with regularization
def unet(input_shape, n_stages=2, n_filters=32, n_filters_const=True, regularization=0):
    """
        Create the model and return it.
 
        :param input_shape: Input shape of the image with the channel, e.g.: (1021, 1442, 1)
        :param n_stages: Number of stages max pooling/upsampling
        :param n_filters: Number of filters for each convolutional layers 
        :param n_filters_const: If False multiply by 2 n_filters at each stages
        :param regularization: L2 regularization
        
        :type input_shape: Tuple of integer (length: 3)
        :type n_stages: int
        :type n_filters: int
        :type n_filters_const: bool
        :type regularization: float

        :return: The model
    """
    
    inputs = Input(input_shape)
    
    conv   = [None] * (2*n_stages+1)
    pool   = [None] * (n_stages)
    up     = [None] * (n_stages)
    merge  = [None] * (n_stages)
    
    if n_filters_const:
        n = [n_filters] * (2*n_stages+1)
        str_filters = str(n_filters)
    else:
        n = np.concatenate((n_filters*2**np.arange(n_stages+1), n_filters*2**np.arange(n_stages-1,-1,-1)))
        str_filters = str(n_filters) + '-' + str(n_filters*2**(n_stages))
    
    # Down
    for l in range(n_stages+1):
        
        if l == 0:
            conv[l] = Conv2D(n[l], 3, activation='relu', padding='same', kernel_initializer='he_normal',
                             kernel_regularizer=regularizers.l2(regularization))(inputs)
        else:
            conv[l] = Conv2D(n[l], 3, activation='relu', padding='same', kernel_initializer='he_normal',
                             kernel_regularizer=regularizers.l2(regularization))(pool[l-1])
        
        conv[l] = Conv2D(n[l], 3, activation='relu', padding='same', kernel_initializer='he_normal',
                         kernel_regularizer=regularizers.l2(regularization))(conv[l])
        
        if l != n_stages:
            pool[l] = MaxPooling2D(pool_size=(2, 2))(conv[l])
            
    # Up
    for i, l in enumerate(np.arange(n_stages+1,2*n_stages+1)):
        
        upsize_y = int(input_shape[0]/2**(n_stages-i-1))
        upsize_x = int(input_shape[1]/2**(n_stages-i-1))
        
        up[i] = Conv2D(n[l], 2, activation='relu', padding='same', kernel_initializer='he_normal',
                       kernel_regularizer=regularizers.l2(regularization))(UpSampling2DBilinear((upsize_y,upsize_x))(conv[l-1]))
        
        merge[i] = concatenate([conv[2*n_stages-l],up[i]], axis=3)
        
        conv[l] = Conv2D(n[l], 3, activation='relu', padding='same', kernel_initializer='he_normal',
                         kernel_regularizer=regularizers.l2(regularization))(merge[i])
        conv[l] = Conv2D(n[l], 3, activation='relu', padding='same', kernel_initializer='he_normal',
                         kernel_regularizer=regularizers.l2(regularization))(conv[l])
   
        
    outputs = Conv2D(1, 1)(conv[2*n_stages])
        
    model = Model(inputs, outputs)
    
    if regularization != 0:
        str_r = '_r'+str(regularization)
    else:
        str_r = ''

    model.name = 'unet_'+str(n_stages)+'s_'+str_filters+'f'+str_r
      
    return model
   

def plot_model(model):
    return SVG(model_to_dot(model).create(prog='dot', format='svg'))