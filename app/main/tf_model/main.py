from predictStrip import imageToNotes, notesToMIDI
import cv2

if __name__ == "__main__":
	image = cv2.imread("/home/boomerang/boomerang/BTech_CS/MIP-Sem6/cloned/Sheet-music-player/app/main/tf_model/Data/Example/ttls.jpg")
	readable = imageToNotes(image)
	corrected = readable
	notesToMIDI(readable)

	for x in readable:
		print(x)