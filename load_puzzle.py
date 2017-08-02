import cv2
import numpy as np
from math import pi
import matplotlib.pyplot as plt

ratio2 = 3
kernel_size = 3
lowThreshold = 30

frame = cv2.imread('puzl.jpg')
sudoku1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
sudoku1 = cv2.blur(sudoku1, (3,3))
edges = cv2.Canny(sudoku1, lowThreshold, lowThreshold*ratio2, kernel_size)

# Apply Hough Line Transform, return a list of rho and theta
cv_pi = pi
thresh = 10
lines = cv2.HoughLines(edges, 2, cv_pi/180, 300, 0, 0)
lines = [line[0] for line in lines]
print len(lines)
if (lines is not None):

	# Define the position of horizontal and vertical line
	pos_hori = 0
	pos_vert = 0
	for rho,theta in lines:
		a = np.cos(theta)
		b = np.sin(theta)
		x0 = a*rho
		y0 = b*rho
		x1 = int(x0 + 1000*(-b))
		y1 = int(y0 + 1000*(a))
		x2 = int(x0 - 1000*(-b))
		y2 = int(y0 - 1000*(a))

		# If b > 0.5, the angle must be greater than 45 degree
		# so we consider that line as a vertical line
		if (b>0.5):
		# Check the position
			if(rho-pos_hori>thresh):
				# Update the positionpos_hori=rho
				pos_hori=rho
				cv2.line(frame,(x1,y1),(x2,y2),(0,0,255),2)
		else:
			if(rho-pos_vert>thresh):
				pos_vert=rho
				cv2.line(frame,(x1,y1),(x2,y2),(0,0,255),2)

		plt.imshow(frame)
		plt.title('img')
		plt.show()