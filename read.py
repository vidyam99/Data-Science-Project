import fitz
import PIL
from PIL import Image
from scipy.misc import imsave
import numpy
import docx
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

import os
def pdf_extraction(filename) :
	f = open(filename.split("\\")[-1].split(".")[0]+'.txt',"w")
	doc = fitz.open(filename)
	for i in range(doc.pageCount) :
		page  = doc.loadPage(i)
		text = page.getText()
		f.write(text)
	for i in range(doc.pageCount) :
		for img in doc.getPageImageList(i) :
				try :
					xref = img[0]
					pix = fitz.Pixmap(doc,xref)
					filename.split("\\")[-1].split(".")[0]
					pix.writePNG(filename.split("\\")[-1].split(".")[0]+str(i)+".png")
				except : 
					print("not an image")
	for file in os.listdir(".") :
		if file.endswith('.png') :
			if file.startswith(filename.split("\\")[-1].split(".")[0]) :
				binarize_image(file,file,)


def binarize_image(img_path, target_path, threshold=200):
    """Binarize an image."""
    image_file = Image.open(img_path)
    image = image_file.convert('L')  # convert image to monochrome
    image = numpy.array(image)
    image = binarize_array(image, threshold)
    imsave(target_path, image)


def binarize_array(numpy_array, threshold=150):
    """Binarize a numpy array."""
    for i in range(len(numpy_array)):
        for j in range(len(numpy_array[0])):
            if numpy_array[i][j] < threshold:
                numpy_array[i][j] = 0
            else:
                numpy_array[i][j] = 255
    return numpy_array


def get_parser():
    """Get parser object for script xy.py."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--input",
                        dest="input",
                        help="read this file",
                        metavar="FILE",
                        required=True)
    parser.add_argument("-o", "--output",
                        dest="output",
                        help="write binarized file hre",
                        metavar="FILE",
                        required=True)
    parser.add_argument("--threshold",
                        dest="threshold",
                        default=200,
                        type=int,
                        help="Threshold when to show white")
    return parser

def png_extraction(filename):
	if filename.endswith('.jpg') or filename.endswith('.png') :
		binarize_image(filename,filename.split("\\")[-1],)
		im = Image.open(filename.split("\\")[-1])
		textt = pytesseract.image_to_string(im)
		f = open(filename.split("\\")[-1].split(".")[0]+".txt",'w',encoding = 'utf8')
		f.write(textt)
		f.close()

def gif_extraction(filename):
	print("hii gif")
	im = Image.open(filename)
	for i in range(1) :
		im.seek(im.n_frames // 1*i)
	print(im.save(filename.split("\\")[-1]))
	binarize_image(filename.split("\\")[-1],filename.split("\\")[-1],)
	im = Image.open(filename.split("\\")[-1])
	textt = pytesseract.image_to_string(im)
	f = open(filename.split("\\")[-1].split(".")[0]+".txt",'w')
	f.write(textt)
	f.close()

def txt_extraction(filename):
	print("hii")

def doc_extraction(filename):
	doc = docx.Document(filename)
	fullText = []
	for para in doc.paragraphs :
		fullText.append(para.text)
	print('\n'.join(fullText))


path = "Training-Set\\"
files  =  os.listdir(path)
for file in files :
	ext = file.split(".")[1]
	if ext == 'pdf' : pdf_extraction(path+file)
	elif ext == 'png' or ext == 'jpg' : png_extraction(path+file)
	elif ext == 'gif' : gif_extraction(path+file)
	elif ext == 'txt' : txt_extraction(path+file)
	elif ext == 'docx' : doc_extraction(path+file)

