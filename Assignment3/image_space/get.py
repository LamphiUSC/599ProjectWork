import cv2
import numpy as np
import json
import random
import os
import pickle

with open("image_files.pickle","r") as f:
    image_files =  pickle.load(f)
with open("image_map.pickle","r") as f1:
    image_map = pickle.load(f1)

def run(query, k=10, mode='bruteforce'):
    if query.startswith('['):
        vec = json.loads(query)
        vec = np.array(vec, dtype=np.float32).reshape(1, 512)
    elif query in image_map:
        vec = image_map[query].reshape(1, 512)
    else:
        return {'error': 'Could not find data for image: ' + query}

    images = []
    if mode == 'bruteforce':
        hist = vec.reshape(512)
        dists = []
        for (i, file) in enumerate(image_files):
            dist = cv2.compareHist(hist, image_map[file], cv2.HISTCMP_INTERSECT)
            dists.append((dist, i))

        top = sorted(dists, reverse=True)[:int(k)]

        for distance, index in top:
            images.append({
                'id': image_files[index],
                'features': image_map[image_files[index]].tolist(),
                'distance': distance
            })

    return images
