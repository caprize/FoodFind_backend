from django.apps import AppConfig
import tensorflow as tf
from tensorflow import keras
import os
import tempfile

from matplotlib import pyplot as plt
import numpy as np



class FastbertConfig(AppConfig):
    name = 'fastbert'
    path_to_pb = "/home/caprize/AIdata/archive/new_model"
    model = tf.saved_model.load(path_to_pb, tags=None)


