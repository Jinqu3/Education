{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "64acc7fb-59de-4ebc-b82f-afb53cc852d2",
   "metadata": {
    "jp-MarkdownHeadingCollapsed": true
   },
   "source": [
    "# Imports"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3379e5ef-2708-48c0-a8ed-95eda57a8aea",
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "import transformers\n",
    "import tensorflow as tf\n",
    "import tqdm.notebook as tqdm\n",
    "import sklearn.model_selection\n",
    "import matplotlib.pyplot as plt"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "299eafa0-89b1-46ba-b659-1bd69880b105",
   "metadata": {},
   "outputs": [],
   "source": [
    "gpus = tf.config.list_physical_devices('GPU')\n",
    "if gpus:\n",
    "    try:\n",
    "        tf.config.experimental.set_memory_growth(gpus[0], True)\n",
    "    except:\n",
    "        pass"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "3588f5af-a33c-4638-90d8-5cb912535790",
   "metadata": {
    "jp-MarkdownHeadingCollapsed": true
   },
   "source": [
    "# Data"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "c468a19b-1395-4afc-b0c5-a799160ea671",
   "metadata": {},
   "source": [
    "Load and prepare your dataset. Dataset should have at least 10k samples in it. Each dataset cannot be used by more than two students."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "bc874386-9591-4f66-bb9a-116f2ec4ff52",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "markdown",
   "id": "714bddcc-c56d-4e61-9147-054f5d7f8e7e",
   "metadata": {
    "jp-MarkdownHeadingCollapsed": true
   },
   "source": [
    "# Backbone"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "c21a2f49-08a6-479a-8db7-a52d4db40d56",
   "metadata": {},
   "source": [
    "Load pretrained model from Hugging Face (or some other model repository if it's more convenient). Model should be trained on Feature Extraction task."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d111bc81-dfb4-47fb-b3d8-42388b84a8cc",
   "metadata": {},
   "outputs": [],
   "source": [
    "backbone = transformers.AutoModel.from_pretrained(...)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "4b81337a-c06e-4b33-9dff-61ff0c6858c9",
   "metadata": {},
   "source": [
    "Load tokenizer to be used with the model"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "4c7e98fb-a356-463d-a856-9b011efdcca1",
   "metadata": {},
   "outputs": [],
   "source": [
    "processor = transformers.AutoImageProcessor.from_pretrained(...)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "c045f3c1-faf9-41fc-af88-a4f49c97ac13",
   "metadata": {
    "jp-MarkdownHeadingCollapsed": true
   },
   "source": [
    "# Feature extraction"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "1025d0d6-3b43-440a-8791-27b3e208e415",
   "metadata": {},
   "source": [
    "Since we will not be training the backbone, extract features from your dataset."
   ]
  },
  {
   "cell_type": "markdown",
   "id": "4a2b4b64-ee2e-4a2a-8d81-161f8bf1aae4",
   "metadata": {},
   "source": [
    "Run the backbone on the images and save the extracted features. Don't forget to process the images. Images don't have to be of the same size, though it would be faster if they were. If the images don't fit in memory, lazily load them from disk"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3449274c-3df3-48b6-afba-e2ad885b4085",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "markdown",
   "id": "2543fcff-46b0-4c05-b297-c3102f998205",
   "metadata": {
    "jp-MarkdownHeadingCollapsed": true
   },
   "source": [
    "# Prepare train/test data"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "2c985c7d-9123-477e-9988-15ff5a7b26eb",
   "metadata": {},
   "source": [
    "Split your data (extracted features and labels) into train and test subsets."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "289a1234-6c10-4fd4-ae37-945ec75d6f19",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "markdown",
   "id": "b1a65639-50d0-4f89-8bfe-33b7a483e406",
   "metadata": {},
   "source": [
    "Prepare `tf.data.Dataset` or some other way for the data to be used during training."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "07849c2e-c7d1-4620-9590-962fa554ed8f",
   "metadata": {},
   "outputs": [],
   "source": [
    "train_X = tf.data.Dataset.from_tensor_slices(X_train)\n",
    "train_y = tf.data.Dataset.from_tensor_slices(y_train)\n",
    "train_dataset = tf.data.Dataset.zip((train_X, train_y)).batch(128)\n",
    "\n",
    "test_X = tf.data.Dataset.from_tensor_slices(X_test)\n",
    "test_y = tf.data.Dataset.from_tensor_slices(y_test)\n",
    "test_dataset = tf.data.Dataset.zip((test_X, test_y)).batch(128)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "e8f74abd-ce1a-4a68-be6c-89b1abd0caa5",
   "metadata": {
    "jp-MarkdownHeadingCollapsed": true
   },
   "source": [
    "# Build the model"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "78885e31-c91e-4ee5-acbf-00a107069da9",
   "metadata": {},
   "source": [
    "Build a simple model. The model should accept an extracted feature vector and return a vector of class logits (or probabilities). Model should only have a couple (or even 1) layers with weights."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ffc94f7a-d2b0-48bf-9f0b-df5d17e01e78",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "markdown",
   "id": "a5cacc4e-9876-40ff-8cd0-f1a4bfbc5c1a",
   "metadata": {},
   "source": [
    "Compile the model. Choose loss and metrics."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "2eecb84f-5dc2-4999-b911-ea0a1c64ec41",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "markdown",
   "id": "3e08006d-be0a-4828-aca9-a9f37218b8de",
   "metadata": {
    "jp-MarkdownHeadingCollapsed": true
   },
   "source": [
    "# Train the model"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "6a30787b-7ac4-4dd3-9ea5-62c94e9aa628",
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "markdown",
   "id": "3980f062-220a-4a11-b9f5-3b0e41804533",
   "metadata": {
    "jp-MarkdownHeadingCollapsed": true
   },
   "source": [
    "# Evaluation"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "4b6008a2-9882-44f2-946c-23827aa5fa49",
   "metadata": {},
   "source": [
    "Evalute the model on test data."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "1b4ddf9e-5710-4c7f-ac58-4d94742c0d14",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "markdown",
   "id": "c96f4ae8-6b6c-4c4d-94dc-be8062b7e982",
   "metadata": {},
   "source": [
    "Plot confusion matrix."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d54494dd-89d4-4f0d-873a-adb4efcbccca",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "markdown",
   "id": "dd5b8f73-9ea8-456c-9768-d82495c2b824",
   "metadata": {},
   "source": [
    "Perform dimensiality reduction and plot the extracted features. Do classes form clusters?"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "56afdf2c-47ab-490d-b1b1-b5858b32a689",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "markdown",
   "id": "dd49c775-eded-4a49-b7f4-9903185a7b9d",
   "metadata": {
    "jp-MarkdownHeadingCollapsed": true
   },
   "source": [
    "# Bonus"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "726c617b-7110-4761-9806-975d5f84bf41",
   "metadata": {},
   "source": [
    "Check if the feature extractor model can be used without a classifier layer (how large is the average feature vector similarity inbetween same in different classes)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "f5bbbaf8-68f6-4aa1-af37-f29b1edae464",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
