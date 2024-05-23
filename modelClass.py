import tensorflow as tf
import tensorflow.keras.utils as utils
import tensorflow.keras.layers as layers
import tensorflow.keras.activations as activations
import tensorflow.keras.optimizers as optimizers
import tensorflow.keras.losses as losses
from tensorflow.train import Checkpoint
import tensorflow.data as data
import os
import datetime

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

		self.model.add(layers.Dense(459, activation=activations.relu))
		self.model.add(layers.Dense(459, activation=activations.relu))

		self.model.add(layers.Dense(256, activation=activations.relu))
		self.model.add(layers.Dense(128, activation=activations.relu))
		self.model.add(layers.Dense(64, activation=activations.relu))
		self.model.add(layers.Dense(32, activation=activations.relu))
		self.model.add(layers.Dense(16, activation=activations.relu))
		self.model.add(layers.Dense(8, activation=activations.relu))
		self.model.add(layers.Dense(4, activation=activations.relu))
		self.model.add(layers.Dense(2, activation=activations.relu))
		self.model.add(layers.Dense(1, activation=activations.relu))

		self.optimizer = optimizers.Adam(learning_rate=0.00001)
		self.loss = losses.CategoricalCrossentropy()
		self.model.compile(
			loss = self.loss,
			optimizer = self.optimizer,
			metrics = ['accuracy'],
		)

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

# model = Model((17, 20))
# model.model.summary()

save_path = "model/"
plotHistoryPath = "modelHistory.json"

playerDataTypes = [
	int(),
	str(),
	str(),
	float(),
	str(),
	str(),
	int(),
	int(),
	int(),
	int(),
	int(),
	int(),
	int(),
	int(),
	float(),
	int(),
	float(),
	int(),
	int(),
	float(),
	float(),
	float(),
	float(),
	float(),
	float(),
	float(),
	int(),
	int(),
	float(),
	int(),
	int(),
	float(),
	str()
	]

playerFiles = os.listdir("data/Lamar Jackson")
trainFiles = []
valFiles = []
for f in playerFiles:
	if f[:4] == "2023":
		valFiles.append(f"data/Lamar Jackson/{f}")
	else:
		trainFiles.append(f"data/Lamar Jackson/{f}")

with open(trainFiles[0], 'r') as f:
	i=0
	for line in f:
		for char in line:
			if char == ",":
				i += 1
	print(i)

train = data.experimental.CsvDataset(trainFiles, record_defaults=playerDataTypes)

for row in train.take(2):
  print(row[0].numpy())

print(train)

# train, validation = utils.image_dataset_from_directory(
# 	'keptPokemon',
# 	label_mode = 'categorical',
# 	batch_size = 256,
# 	image_size = (239, 239),
# 	seed = 69,
# 	validation_split = 0.15,
# 	subset = 'both'
# )

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