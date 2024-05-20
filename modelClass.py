import tensorflow as tf
import tensorflow.keras.utils as utils
import tensorflow.keras.layers as layers
import tensorflow.keras.activations as activations
import tensorflow.keras.optimizers as optimizers
import tensorflow.keras.losses as losses
from tensorflow.train import Checkpoint
import tensorflow.data as data

def saveStuff(model, save_path, plotHistoryPath, history):
	print(f"Saving model to {save_path}")
	model.model.save(save_path)

	import json
	print(f"Saving training history to {plotHistoryPath}")

	old_history = {
		"accuracy": [],
		"loss": [],
		"val_accuracy": [],
		"val_loss": [],
	}
	try:
		with open(plotHistoryPath, "r") as f:
			old_history = json.load(f)
	except (FileNotFoundError, json.decoder.JSONDecodeError):
		pass

	if old_history is not None:
		old_history["accuracy"] += history.history["accuracy"]
		old_history["loss"] += history.history["loss"]
		old_history["val_accuracy"] += history.history["val_accuracy"]
		old_history["val_loss"] += history.history["val_loss"]

	with open(plotHistoryPath, "w") as f:
		json.dump(old_history, f, indent=4)

class Model:
	def __init__(self, inputSize):
		self.model = tf.keras.Sequential()

		self.model.add(layers.Flatten())

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

model = Model(1, 17, 3)
# this hsould be 17 by number of inputs (stride length?)