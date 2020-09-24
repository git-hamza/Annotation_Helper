import xml.etree.ElementTree as ET 
import os
from os import listdir
from os.path import isfile, join
import imutils
import cv2
import argparse

def resize_img(frame,resize_percentage=50):
    width = int(frame.shape[1] * resize_percentage/ 100)
    height = int(frame.shape[0] * resize_percentage / 100)
    dim = (width, height)
    resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    return resized

def resize_img_folder(ImagesPath,OUT_IMGS_PATH,resize_percentage=50):
	onlyfiles = [ f for f in listdir(ImagesPath) if isfile(join(ImagesPath,f)) ]
	for n in range(0,len(onlyfiles)):
		print(join(ImagesPath, onlyfiles[n]))
		image = cv2.imread(join(ImagesPath, onlyfiles[n]))
		image = resize_img(image,resize_percentage)
		output_path = OUT_IMGS_PATH + onlyfiles[n]
		cv2.imwrite(output_path,image)
	print("Done")

def resize_annotations(IN_ANN,OUT_IMGS_PATH,resize_percentage,image_format = ".jpg"):
	for xml_file in os.listdir(IN_ANN):
		tree = ET.parse(os.path.join(IN_ANN,xml_file))  
		root = tree.getroot()
		
		bndbox = root.findall('object')
		siize = root.findall('size')
		wd = int(siize[0][0].text)
		ht = int(siize[0][1].text)
		imgg_namee = xml_file.split('.')[0] + image_format
		imggg = cv2.imread(OUT_IMGS_PATH+imgg_namee)
		new_wd = imggg.shape[1]
		new_he = imggg.shape[0]

		siize[0][0].text = str(new_wd)
		siize[0][1].text = str(new_he)
		for bb in bndbox:
			xmn = int(int(bb[4][0].text) * resize_percentage/100)
			ymn = int(int(bb[4][1].text) * resize_percentage/100)
			xmx = int(int(bb[4][2].text) * resize_percentage/100)
			ymx = int(int(bb[4][3].text) * resize_percentage/100)
			bb[4][0].text = str(xmn)
			bb[4][1].text = str(ymn)
			bb[4][2].text = str(xmx)
			bb[4][3].text = str(ymx)

		tree.write(os.path.join(IN_ANN,xml_file))
	print("Done")

def main():
	ap = argparse.ArgumentParser()
	ap.add_argument("-a","--annotations", required=True,type =str,help="path to annotations folder")
	ap.add_argument("-i","--images", required=True,type =str,help="path to images folder")
	args = vars(ap.parse_args())

	resize_percentage = 50
	image_format = ".jpg"
	ImagesPath = args["images"]
	OUT_IMGS_PATH = 'Output_Images/'
	IN_ANN = args["annotations"]

	if not os.path.isdir(OUT_IMGS_PATH):
		os.mkdir(OUT_IMGS_PATH)

	resize_img_folder(ImagesPath,OUT_IMGS_PATH,resize_percentage)
	resize_annotations(IN_ANN,OUT_IMGS_PATH,resize_percentage,image_format)

if __name__ == '__main__':
	main()