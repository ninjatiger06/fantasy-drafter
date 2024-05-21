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

		self.model.add(layers.Dense(340, activation=activations.relu))

		self.optimizer = optimizers.Adam(learning_rate=self.lr_scheduler)
		# self.optimizer = optimizers.Adam(learning_rate=0.00001)
		self.loss = losses.CategoricalCrossentropy()
		self.model.compile(
			loss = self.loss,
			optimizer = self.optimizer,
			metrics = ['accuracy'],
		)

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

model = Model(17, 20, 3)
model.model.summary()

save_path = "model/"
plotHistoryPath = "modelHistory.json"

train, validation = utils.image_dataset_from_directory(
	'keptPokemon',
	label_mode = 'categorical',
	batch_size = 256,
	image_size = (239, 239),
	seed = 69,
	validation_split = 0.15,
	subset = 'both'
)

train = train.cache().prefetch(buffer_size = data.AUTOTUNE)
validation = validation.cache().prefetch(buffer_size = data.AUTOTUNE)

# load previous weights if they exist
model.model.load_weights(save_path)

cpCallback = tf.keras.callbacks.ModelCheckpoint(filepath = save_path, save_weights_only = True, verbose = 1)

history = model.model.fit(
	train,
	batch_size = 256,
	epochs = 30,
	verbose = 1,
	validation_data = validation,
	validation_batch_size = 32
)

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