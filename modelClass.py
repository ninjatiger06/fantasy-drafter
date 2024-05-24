import tensorflow as tf
import tensorflow.keras.utils as utils
import tensorflow.keras.layers as layers
import tensorflow.keras.activations as activations
import tensorflow.keras.optimizers as optimizers
import tensorflow.keras.losses as losses
from tensorflow.train import Checkpoint
from tensorflow.data import Dataset
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

def datasetConfig(trainLst, valLst):
	# allTrain = Dataset()
	# allValid = Dataset()

	trains = []
	labels = []

	first = 0
	last = 16
	while last <= len(trainLst) - 1:
		tempTrains = []
		tempLabels = []
		print(first, last, "\n", trainLst[first], trainLst[last])
		for filename in trainLst[first:last]:
			with open(filename, 'r') as f:
				for line in f:
					dataLst = line.split(', ')
				dataPts = []
				for i in range(len(dataLst)):
					if i == 25:
						y = float(dataLst[i])
					else:
						dataPts.append(float(dataLst[i]))
				trainTf = [tf.convert_to_tensor(dataPts)]
				# trainDs = Dataset.from_tensor_slices(trainTf)
				trainLabelsTf = [tf.convert_to_tensor(float(y), dtype=tf.float32)]
				# trainLabelsDs = Dataset.from_tensor_slices(trainLabelsTf)
				for train, label in list(zip(trainTf, trainLabelsTf)):
					tempTrains.append(train)
					tempLabels.append(label)
		trains.append(tempTrains)
		labels.append(tempLabels)
		first += 1
		last += 1

	valids = []
	valLabels = []

	first = 0
	last = 16
	while last <= len(valLst) - 1:
		tempVals = []
		tempValLabels = []
		for filename in valLst[first:last]:
			with open(filename, 'r') as f:
				for line in f:
					dataLst = line.split(', ')
				dataPts = []
				for i in range(len(dataLst)):
					if i == 25:
						y = float(dataLst[i])
					else:
						dataPts.append(float(dataLst[i]))
				valTf = [tf.convert_to_tensor(dataPts)]
				valLabelsTf = [tf.convert_to_tensor(float(y), dtype=tf.float32)]
				for val, valLabel in list(zip(valTf, valLabelsTf)):
					tempVals.append(val)
					tempValLabels.append(valLabel)
		valids.append(tempVals)
		valLabels.append(tempValLabels)
		first += 1
		last += 1

	trainDs = Dataset.from_tensor_slices(trains)
	labelsDs = Dataset.from_tensor_slices(labels)

	valsDs = Dataset.from_tensor_slices(valids)
	valLabelsDs = Dataset.from_tensor_slices(valLabels)

	allTrainDs = Dataset.zip((trainDs, labelsDs))
	allTrainDs = allTrainDs.batch(256)
	allValidDs = Dataset.zip((valsDs, valLabelsDs))
	allValidDs = allValidDs.batch(256)

	return allTrainDs, allValidDs

class Model:
	def __init__(self, inputSize):
		self.model = tf.keras.Sequential()

		# self.model.add(layers.Flatten())

		self.model.add(layers.Dense(544, activation=activations.relu))
		self.model.add(layers.Dense(544, activation=activations.relu))

		self.model.add(layers.Dense(512, activation=activations.relu))
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

model = Model((None, 16, 32))
model.model.build((None, 16, 32))
model.model.summary()

save_path = "model/"
plotHistoryPath = "modelHistory.json"

playerFiles = os.listdir("data/Lamar Jackson")
trainFiles = []
valFiles = []
for f in playerFiles:
	if f[:4] == "2023":
		valFiles.append(f"data/Lamar Jackson/{f}")
	else:
		trainFiles.append(f"data/Lamar Jackson/{f}")

train, validation = datasetConfig(trainFiles, valFiles)

names = [
	"week",
	"age",
	"team",
	"opp",
	"teamScore",
	"oppScore",
	"Cmp",
	"passAtt",
	"Inc",
	"Cmp%",
	"passYds",
	"passTD",
	"Int",
	"Pick6",
	"TD%",
	"Int%",
	"Rate",
	"Sk",
	"skYds",
	"Sk%",
	"passY/A",
	"AY/A",
	"ANY/A",
	"Y/C",
	"passSucc%",
	"PPR",
	"rushAtt",
	"rushYds",
	"rushY/A",
	"rushTD",
	"1D",
	"rushSucc%",
	"Pos."
]

for row in train.take(1):
  print(f"\n ROW: {len(row)}")
  print(row)

train = train.cache().prefetch(buffer_size = data.AUTOTUNE)
validation = validation.cache().prefetch(buffer_size = data.AUTOTUNE)

# load previous weights if they exist
# model.model.load_weights(save_path)

cpCallback = tf.keras.callbacks.ModelCheckpoint(filepath = save_path, save_weights_only = True, verbose = 1)

history = model.model.fit(
	train,
	batch_size = 256,
	epochs = 5,
	verbose = 1,
	validation_data = validation,
	validation_batch_size = 32,
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