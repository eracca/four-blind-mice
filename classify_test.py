import tensorflow as tf
import numpy as np

labels = ["wait", "walk"] 
model_file = "retrained_graph.pb"
image_height = 224
image_width = 224
input_mean = 128
input_std = 128
input_layer = "input"
output_layer = "final_result"

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

def classify_pic(graph, image_file):
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
	print(labels[top_k[0]])
	return(top_k[0])


graph = load_graph(model_file)
classify_pic(graph, "pic_9845.jpg")




