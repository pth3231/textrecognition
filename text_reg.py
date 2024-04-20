import cv2
import pytesseract

class Model():
	def __init__(self, img_path: str, kernel_shape: tuple = (20, 20)):
		pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
		self.img = cv2.imread(img_path)
		# Convert the image to gray scale
		self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
		# Performing OTSU threshold
		self.ret, self.thresh1 = cv2.threshold(self.gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

		# Specify structure shape and kernel size. 
		# Kernel size increases or decreases the area of the rectangle to be detected.
		self.rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (22, 22))

		# Applying dilation on the threshold image
		self.dilation = cv2.dilate(self.thresh1, self.rect_kernel, iterations = 1)

		# Finding contours
		self.contours, self.hierarchy = cv2.findContours(self.dilation, 
											cv2.RETR_EXTERNAL, 
											cv2.CHAIN_APPROX_NONE)
		# Creating a copy of image
		self.im2 = self.img.copy()

	# By default, the predict() function will trying to open the recognized.txt file
	def predict(self):
		# A text file is created and flushed
		file = open("./test/recognized.txt", "w+")
		file.write("")
		file.close()
		print(self.contours)
		# Looping through the identified contours then rectangular part is cropped and passed on to pytesseract for extracting text from it
		# Extracted text is then written into the text file
		for self.cnt in self.contours:
			x, y, w, h = cv2.boundingRect(self.cnt)
			# Drawing a rectangle on copied image
			rect = cv2.rectangle(self.im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
			# Cropping the text block for giving input to OCR
			cropped = self.im2[y:y + h, x:x + w]
			# Open the file in append mode
			file = open("./test/recognized.txt", "a")
			# Apply OCR on the cropped image
			text = pytesseract.image_to_string(cropped)
			file.write(text)
			file.close()
