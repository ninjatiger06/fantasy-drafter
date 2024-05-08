import tensorflow as tf
import tensorflow.keras.utils as utils
import tensorflow.keras.layers as layers
import tensorflow.keras.activations as activations
import tensorflow.keras.optimizers as optimizers
import tensorflow.keras.losses as losses
from tensorflow.train import Checkpoint
import tensorflow.data as data

class Model:
	def __init__(self):
		self.model = tf.keras.Sequential()

		self.model.add(layers.Flatten())