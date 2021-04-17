from predictStrip import imageToNotes

if __name__ == "__main__":
	image = cv2.imread("/home/boomerang/boomerang/BTech_CS/MIP-Sem6/ComputerVision/tf-end-to-end-master/Data/Example/o2j.jpg")

	cv2.imshow("input", image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	readable = imageToNotes(image)

	for x in readable:
		print(x)