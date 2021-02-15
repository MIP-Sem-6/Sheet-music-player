import cv2
import numpy as np

def resize(img, scale):
	scale_percent = scale # percent of original size
	width = int(img.shape[1] * scale_percent / 100)
	height = int(img.shape[0] * scale_percent / 100)
	dim = (width, height)
	
	resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
	return resized

img = cv2.imread("o2j.jpg", 0)
# img = resize(img, 100)
w_sheet, h_sheet = img.shape[::1]

clef = cv2.imread('clef.jpg',0)
w_clef, h_clef = clef.shape[::-1]

res = cv2.matchTemplate(img,clef,cv2.TM_CCOEFF_NORMED)
threshold = 0.9
loc = np.where( res >= threshold)

# for pt in zip(*loc[::-1]):
#     cv2.rectangle(img, pt, (pt[0] + w_clef, pt[1] + h_clef), (0,255,255), 2)

music_lines = []
for pt in zip(*loc[::-1]):
	print(pt)
	line = img[pt[1] :pt[1] + h_clef]
	music_lines.append(line)
	# cv2.imshow(str(pt),line)

line = music_lines[0]
print(line)

cv2.imwrite("image.jpg", line)

inverse = cv2.bitwise_not(line)

horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25,1))
detected_lines = cv2.morphologyEx(inverse, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    cv2.drawContours(line, [c], -1, (255,255,255), 2)

repair_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,6))
result = 255 - cv2.morphologyEx(255 - line, cv2.MORPH_CLOSE, repair_kernel, iterations=1)


# print(w_sheet, h_sheet)

# print(img)
cv2.imshow('line',music_lines[0])
# print(music_lines[0])
# cv2.imshow('Detected',img_rgb)
# cv2.imshow(music_lines[0])
# cv2.imshow("clef", clef)
# cv2.imshow("sheet",img)
cv2.imshow("thresh",result)


# cv2.imshow("laplacian",laplacian)
# cv2.imshow("sobelX",sobelx)
# cv2.imshow("sobelY",sobely)

cv2.waitKey(0)

