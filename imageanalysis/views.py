# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from .form import SearchForm
import os

import tensorflow.python.platform
from six.moves import urllib
import os.path
import re
import sys
import tarfile
import numpy as np
import tensorflow as tf
from tensorflow.python.platform import gfile


FLAGS = tf.app.flags.FLAGS
DIR = './imageanalysis/static/tmpimage/'
#print FLAGS.model_dir
class NodeLookup(object):
  """Converts integer node ID's to human readable labels."""
  def __init__(self,
               label_lookup_path=None,
               uid_lookup_path=None):
    if not label_lookup_path:
      label_lookup_path = os.path.join(
          DIR, 'imagenet_2012_challenge_label_map_proto.pbtxt')
    if not uid_lookup_path:
      uid_lookup_path = os.path.join(
          DIR, 'imagenet_synset_to_human_label_map.txt')
    self.node_lookup = self.load(label_lookup_path, uid_lookup_path)
  def load(self, label_lookup_path, uid_lookup_path):
    if not gfile.Exists(uid_lookup_path):
      tf.logging.fatal('File does not exist %s', uid_lookup_path)
    if not gfile.Exists(label_lookup_path):
      tf.logging.fatal('File does not exist %s', label_lookup_path)
    # Loads mapping from string UID to human-readable string
    proto_as_ascii_lines = gfile.GFile(uid_lookup_path).readlines()
    uid_to_human = {}
    p = re.compile(r'[n\d]*[ \S,]*')
    for line in proto_as_ascii_lines:
      parsed_items = p.findall(line)
      uid = parsed_items[0]
      human_string = parsed_items[2]
      uid_to_human[uid] = human_string
    # Loads mapping from string UID to integer node ID.
    node_id_to_uid = {}
    proto_as_ascii = gfile.GFile(label_lookup_path).readlines()
    for line in proto_as_ascii:
      if line.startswith('  target_class:'):
        target_class = int(line.split(': ')[1])
      if line.startswith('  target_class_string:'):
        target_class_string = line.split(': ')[1]
        node_id_to_uid[target_class] = target_class_string[1:-2]
    # Loads the final mapping of integer node ID to human-readable string
    node_id_to_name = {}
    for key, val in node_id_to_uid.items():
      if val not in uid_to_human:
        tf.logging.fatal('Failed to locate: %s', val)
      name = uid_to_human[val]
      node_id_to_name[key] = name
    return node_id_to_name
  def id_to_string(self, node_id):
    if node_id not in self.node_lookup:
      return ''
    return self.node_lookup[node_id]

def create_graph():
  with gfile.FastGFile(os.path.join(
      DIR, 'classify_image_graph_def.pb'), 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')

def run_inference_on_image(image):
  if not gfile.Exists(image):
    tf.logging.fatal('File does not exist %s', image)
  image_data = gfile.FastGFile(image, 'rb').read()

  create_graph()
  with tf.Session() as sess:

    softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')
    predictions = sess.run(softmax_tensor,
                           {'DecodeJpeg/contents:0': image_data})
    predictions = np.squeeze(predictions)
    # Creates node ID --> English string lookup.
    node_lookup = NodeLookup()
    top_k = predictions.argsort()[-1:][::-1]
    #for node_id in top_k:
    node_id = top_k[0]
    human_string = node_lookup.id_to_string(node_id)
    score = predictions[node_id]
    print('%s (score = %.5f)' % (human_string, score))
    return (human_string, score)

def runclassimg(f):

  (str, score) = run_inference_on_image(f)
  return str, score

#str = runclassimg('/home/moon/tmp/tmpimg.jpg')
#print str

def home(request):

    return render(
            request,
            'index.html'
    )

def poweranalysis(request):

    if request.method == 'POST':
            form = SearchForm(request.POST, request.FILES)
            search_form = SearchForm()
            if form.is_valid():
                imagedir = './imageanalysis/static/tmpimage/tmpimg.jpg'
                print imagedir
                handle_uploaded_file(request.FILES['image'], imagedir)

                str, score = runclassimg(imagedir)
                context = {
                'image': str,
                'score': score*100,
                'search_form': search_form,
                }


            return render(
                request,
                'imageanalysis.html',
                context

            )

    else:
        search_form = SearchForm()
        context = {
            'search_form': search_form,
        }
        return render(
                request,
                'imageanalysis.html',
                context
        )


def handle_uploaded_file(f, imagedir):
    with open(imagedir,'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

