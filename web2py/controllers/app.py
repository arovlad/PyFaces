# -*- coding: utf-8 -*-
import mtcnn
from mtcnn import MTCNN
import PIL
import time
import re
from io import BytesIO
import base64
import numpy as np
from PIL import Image
from os import listdir
import os.path
from keras.optimizers import *
from keras.models import load_model
from matplotlib import pyplot
from numpy import savez_compressed
from numpy import asarray
from numpy import load
from numpy import expand_dims
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import Normalizer
from sklearn.svm import SVC
from random import choice


def result():
    start_time = time.time()
    data = load(os.path.join(request.folder, '..', '..', '..', 'our_faces.npz'))
	# load face embeddings
    data = load(os.path.join(request.folder, '..', '..', '..', 'our_faces_embeddings.npz'))
    trainX, trainy = data['arr_0'], data['arr_1']
	# normalize input vectors
    in_encoder = Normalizer(norm='l2')
    trainX = in_encoder.transform(trainX)
	# label encode targets
    out_encoder = LabelEncoder()
    out_encoder.fit(trainy)
    trainy = out_encoder.transform(trainy)
	# fit model
    model = SVC(kernel='linear', probability=True)
    model.fit(trainX, trainy)
	# test model on a random example from the test dataset
    modelK = load_model(os.path.join(request.folder, '..', '..', '..', 'facenet_keras.h5'))
    image = Image.open(BytesIO(base64.b64decode(re.sub('^data:image/.+;base64,', '', request.post_vars["imagedata"]))))
    #convert to base 64
    temp_image = image;
    temp_image.thumbnail((160, 160), Image.ANTIALIAS)
    buffered = BytesIO()
    temp_image.save(buffered, format="JPEG")
    ret_attr_orig_image = base64.b64encode(buffered.getvalue())
    #end convert
    pixels=np.array(image)
    detector = MTCNN()
    results=detector.detect_faces(pixels)
    if not results:
        return dict(prediction="no one")
    x1, y1, width, height = results[0]['box']
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    face = pixels[y1:y2, x1:x2]
    image = Image.fromarray(face)
    image = image.resize((160, 160))
    # convert to base64 for output
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    ret_attr_image_face = base64.b64encode(buffered.getvalue())
    # end convert
    random_face_pixels = np.asanyarray(image)
    face_pixels = random_face_pixels.astype('float32')
	# standardize pixel values across channels (global)
    mean, std = face_pixels.mean(), face_pixels.std()
    face_pixels = (face_pixels - mean) / std
	# transform face into one sample
    samples = expand_dims(face_pixels, axis=0)
	# make prediction to get embedding
    yhat = modelK.predict(samples)
	# prediction for the face
    samples = expand_dims(yhat[0], axis=0)
    yhat_class = model.predict(samples)
    yhat_prob = model.predict_proba(samples)
	# get name
    class_index = yhat_class[0]
    class_probability = yhat_prob[0,class_index] * 100
    predict_names = out_encoder.inverse_transform(yhat_class)
    return dict(prediction=predict_names[0], probability=class_probability, orig_image=ret_attr_orig_image, image_face=ret_attr_image_face, time_elapsed=(time.time() - start_time))
