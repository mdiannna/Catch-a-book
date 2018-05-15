# TODO: pip install Pillow
import PIL.Image
# Daca nu merge PIL.image, incearca urmatoarea varianta:
# import Image 
# TODO: pip install pytesseract
import pytesseract
from settings import LANGUAGE, UPLOAD_FOLDER, RECOGNIZE_FOLDER, IMG_NAME
# import app.isbn
import isbn
import os
from app import app


def raw_recognize():

	language = LANGUAGE

	path_in = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),app.config['UPLOAD_FOLDER'], IMG_NAME))
	# path_in = path_in.replace('/', '\\')
	path_in = os.path.normpath(path_in)
	img_name = IMG_NAME
	path_out = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), RECOGNIZE_FOLDER))
	# path_out.replace('/', '\\')

	file_name = img_name

	file_name = file_name.replace(".png", ".txt")
	file_name = file_name.replace(".jpg", ".txt")
	file_name = file_name.replace(".gif",  ".txt")
	file_name = file_name.replace(".jpeg", ".txt")

	print (path_in)
	recog_text = pytesseract.image_to_string(PIL.Image.open(path_in), lang=language)
	print ("recognized text:", recog_text)
	print_to_file(path_out, file_name, recog_text)
	return recog_text

def print_to_file(path, file_name, text):
	file = open(path + file_name, "w")
	file.write(text)
	file.close()
		

def recognize_ISBN(filename):
	raw_text = raw_recognize()
	filtered_ISBN = isbn.filter_raw_ISBN(raw_text)
	if isbn.check_ISBN(filtered_ISBN):
		return filtered_ISBN
	else:
		return None