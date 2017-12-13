#proof of concept for Team 131

import tensorflow as tf
import numpy as np
import pygame.camera
import RPi.GPIO as GPIO
from time import sleep
import os, sys
import pygame

#constants
labels = ["wait", "walk"] 
model_file = "retrained_graph.pb"
image_height = 224
image_width = 224
input_mean = 128
input_std = 128
input_layer = "input"
output_layer = "final_result"

PATH = '/'
WALK_BUTTON = 17
INDICATOR = 18
OP_BUTTON = 23
walk_file = 'audio/Walk.wav'
wait_file = 'audio/Wait.wav'

def load_graph(model_file):
	graph = tf.Graph()
	graph_def = tf.GraphDef()	
	with open(model_file, "rb") as f:
		graph_def.ParseFromString(f.read())
	with graph.as_default():
		tf.import_graph_def(graph_def)
	return graph

def read_tensor_from_image_file(file_name, input_height=299, input_width=299,
				input_mean=0, input_std=255):
	input_name = "file_reader"
	output_name = "normalized"
	file_reader = tf.read_file(file_name, input_name)
	image_reader = tf.image.decode_jpeg(file_reader, channels = 3, name='jpeg_reader')
	float_caster = tf.cast(image_reader, tf.float32)
	dims_expander = tf.expand_dims(float_caster, 0);
	resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
	normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
	sess = tf.Session()
	result = sess.run(normalized)
	return result

def read_tensor_from_image(image, input_height=299, input_width=299, input_mean=0, input_std=255):	
	image_reader = image
	float_caster = tf.cast(image_reader, tf.float32)
	dims_expander = tf.expand_dims(float_caster, 0);
	resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
	normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
	sess = tf.Session()
	result = sess.run(normalized)
	return result

def classify_pic(graph, image_file):
	print("classifying " + image_file)
	input_layer = "input"
	output_later = "final_result"
	t = read_tensor_from_image_file(image_file, image_height, image_width,
					input_mean, input_std)
	input_name = "import/" + input_layer
	output_name = "import/" + output_layer
	input_operation = graph.get_operation_by_name(input_name);
	output_operation = graph.get_operation_by_name(output_name);
	with tf.Session(graph=graph) as sess:
		results = sess.run(output_operation.outputs[0], {input_operation.outputs[0]: t})
	results = np.squeeze(results)
	top_k = results.argsort()[-5:][::-1]
	for i in top_k:
		print(labels[i], results[i])		
	return(top_k[0])

def crossing():
	wait_sound.play()
	walk = False
	while not walk:
		#wait for walk sign to turn on
		img = camera.get_image()
		pygame.image.save(img,'crossing_pic.jpg')
		walk = classify_pic(graph,'crossing_pic.jpg')	
		if walk:
			walk_sound.play()	
			print("Begin crossing.")	
		else:
			wait_sound.play()
			print("Wait to cross.")
	while walk:
		img = camera.get_image()
		pygame.image.save(img,'crossing_pic.jpg')
		walk = classify_pic(graph,'crossing_pic.jpg')
		if walk:
			walk_sound.play()
			print("Continue crossing.")
		else:
			wait_sound.play()	
			print("Stop crossing.")


def setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(WALK_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(INDICATOR, GPIO.OUT) 
	GPIO.output(INDICATOR, GPIO.LOW)
	global graph
	graph = load_graph(model_file)
	pygame.init()
	pygame.mixer.init()
	global walk_sound
	global wait_sound
	walk_sound = pygame.mixer.Sound(walk_file)
	wait_sound = pygame.mixer.Sound(wait_file)
	pygame.camera.init()
	global camera
	camera = pygame.camera.Camera(pygame.camera.list_cameras()[0], (1080, 1080))
	camera.start()
	#ready to go
	GPIO.output(INDICATOR, GPIO.HIGH)
	sleep(2)
	GPIO.output(INDICATOR, GPIO.LOW)
	print("Ready to go")


def main():
	#run setup, play light to indicate readiness
	setup()
	walk_button = False
	while True:	
		try:
			#wait for walk button to be pressed to start crossing
			while not walk_button:
				try: 
					walk_button  = GPIO.wait_for_edge(WALK_BUTTON, GPIO.RISING)
					if walk_button:
						print("Walk sign on")
				except KeyboardInterrupt:
					break
			crossing()
			walk_button = False
		except KeyboardInterrupt:
			break


main()	
		
