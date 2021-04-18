from predictStrip import imageToNotes, notesToMIDI
import cv2

if __name__ == "__main__":
	readable = imageToNotes(image)
	notesToMIDI(readable)

	for x in readable:
		print(x)