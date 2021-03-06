import tensorflow as tf
from tensorflow.python.keras.layers import concatenate

from ..custom_layers import Reroute
from ..feature_extractors.darknet19 import conv_block


# @TODO : create a loop for fine_grained layers
def yolov2_detector(feature_map,
                    fine_grained_layers):
  """ Original YOLOv2 Implementation
  """
  layer = fine_grained_layers[0]
  with tf.name_scope("Detector"):
    x = conv_block(feature_map, 1024, (3, 3), name="DetectConv2d_1")
    x = conv_block(x, 1024, (3, 3), name="DetectConv2d_2")
    x2 = x

    connected_layer = conv_block(layer, 64, (1, 1), name="FineGrained_0")
    rerouted_layer = Reroute(block_size=2,
                             name='RerouteLayer')(connected_layer)

    x = concatenate([rerouted_layer, x2], name="ConcatLayer")
    x = conv_block(x, 1024, (3, 3), name="DetectConv2d_3")

    return x
