import argparse
import tensorflow as tf
import ctc_utils
import cv2
import numpy as np
import logging

logging.getLogger('tensorflow').disabled = True

tf.reset_default_graph()
sess=tf.InteractiveSession()

image_loc = "./Data/Example/1.jpg" 
voc_file = "./Data/vocabulary_semantic.txt"
model = "./SemanticModel/semantic_model.meta"


def splitToStrips(image):
	img=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	og_img = img

	img = cv2.bitwise_not(img)
	th2 = cv2.adaptiveThreshold(img,255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,15,-2)

	horizontal = th2
	vertical = th2
	rows,cols = horizontal.shape

	#inverse the image, so that lines are black for masking
	horizontal_inv = cv2.bitwise_not(horizontal)
	#perform bitwise_and to mask the lines with provided mask
	masked_img = cv2.bitwise_and(img, img, mask=horizontal_inv)
	#reverse the image back to normal
	masked_img_inv = cv2.bitwise_not(masked_img)

	horizontalsize = int(cols / 30)
	horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontalsize,1))
	horizontal = cv2.erode(horizontal, horizontalStructure, (-1, -1))
	horizontal = cv2.dilate(horizontal, horizontalStructure, (-1, -1))

	cv2.imshow("horizontal", horizontal)
	h,w = og_img.shape
	print(h, w)

	# Calculate horizontal projection
	proj = np.sum(horizontal,1)

	max_val = max(proj)
	for i in range(len(proj)):
		if proj[i] < max_val/5:
			proj[i] = 0
		else:
			proj[i] = w

	print(proj)

	zeroes = []
	gaps = []
	cnt = 0 
	start = 0
	for i in range(len(proj)):
		if proj[i] != 0:
			if cnt > 1:
				zeroes.append(cnt)
				gaps.append((start, i))
				cnt = 0
			start = i + 1
		cnt += 1
		if i == len(proj) - 1 and proj[i] == 0:
			zeroes.append(cnt)
			gaps.append((start, i))

	print(zeroes)
	# print(gaps)


	mean = int(np.average(zeroes))
	# print(mean)

	mode = max(set(zeroes), key=zeroes.count)
	# print(mode)

	average_gap = (mean + mode) // 2
	print(average_gap)
	big_gaps = []
	for i in range(len(zeroes)):
		if zeroes[i] > average_gap: 
			big_gaps.append(gaps[i])

	# print(big_gaps)
	
	strips = []
	for i in range(len(big_gaps)):
		if i == (len(big_gaps) - 1):
			if big_gaps[i][1] + 5 < h:
				strip = og_img[max(0, big_gaps[i][1] - int(h/40)): h - 1, :]
				strips.append(strip)
			break
				
		strip = og_img[max(0, big_gaps[i][1] - int(h/40)): min(h, big_gaps[i+1][0] + int(h/40)), :]
		strips.append(strip)

	return strips

def getReadableNotes(strips):
	# Read the dictionary
	dict_file = open(voc_file,'r')
	dict_list = dict_file.read().splitlines()
	int2word = dict()
	for word in dict_list:
		word_idx = len(int2word)
		int2word[word_idx] = word
	dict_file.close()


	# Restore weights
	saver = tf.train.import_meta_graph(model)
	saver.restore(sess,model[:-5])

	graph = tf.get_default_graph()

	input = graph.get_tensor_by_name("model_input:0")
	seq_len = graph.get_tensor_by_name("seq_lengths:0")
	rnn_keep_prob = graph.get_tensor_by_name("keep_prob:0")
	height_tensor = graph.get_tensor_by_name("input_height:0")
	width_reduction_tensor = graph.get_tensor_by_name("width_reduction:0")
	logits = tf.get_collection("logits")[0]


	# Constants that are saved inside the model itself
	WIDTH_REDUCTION, HEIGHT = sess.run([width_reduction_tensor, height_tensor])

	decoded, _ = tf.nn.ctc_greedy_decoder(logits, seq_len)

	readable_notes = []
	for strip in strips:
		strip = ctc_utils.resize(strip, HEIGHT)
		strip = ctc_utils.normalize(strip)
		strip = np.asarray(strip).reshape(1,strip.shape[0],strip.shape[1],1)

		seq_lengths = [ strip.shape[2] / WIDTH_REDUCTION ]

		prediction = sess.run(decoded,
							feed_dict={
								input: strip,
								seq_len: seq_lengths,
								rnn_keep_prob: 1.0,
							})

		str_predictions = ctc_utils.sparse_tensor_to_strs(prediction)

		readable_notes_strip = []
		for w in str_predictions[0]:	
			readable_notes_strip.append(int2word[w]),

		readable_notes.append(readable_notes_strip)

	return readable_notes

def imageToNotes(image):
	strips = splitToStrips(image)
	readable = getReadableNotes(strips)
	return readable
