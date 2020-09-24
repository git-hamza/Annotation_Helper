import xml.etree.ElementTree as ET 
import os
import argparse

def list_all_labels(IN_ANN,Count_Flag=False):
	##Shows you all the unique labels in xmls
	Labels = {}
	for xml_file in os.listdir(IN_ANN):
		tree = ET.parse(os.path.join(IN_ANN,xml_file))  
		root = tree.getroot()
		bndbox = root.findall('object')
		for bb in bndbox:
			txt = bb[0].text
			if len(Labels) ==0:
				Labels[txt] = 1
			else:
				if txt in Labels.keys():
					Labels[txt] = Labels[txt] + 1
					pass
				else:	
					Labels[txt] = 1
	if Count_Flag == False:
		print("Number of Labels : ", (len(Labels)))
		print("####__All Labels__######")
		for label in Labels.keys():
			print(label)
	else:
		return Labels

def count_of_each_label(IN_ANN):
	##Shows you thr number of instances of each unique labels
	Labels = list_all_labels(IN_ANN,Count_Flag=True)
	Labels = sorted(Labels.items(), key=lambda kv: kv[1])
	Labels.reverse()
	for label in Labels:
		print(label)

def change_label_name(IN_ANN,before='',after=''):
	##You can change labels name in all xmls
	for xml_file in os.listdir(IN_ANN):
		tree = ET.parse(os.path.join(IN_ANN,xml_file))  
		root = tree.getroot()
		bndbox = root.findall('object')
		for bb in bndbox:
			txt = bb[0].text
			if txt == before:
				bb[0].text = after
		tree.write(os.path.join(IN_ANN,xml_file))
	print("Done")

def bbox_exceed_image_shape(IN_ANN):
	##tackle the error caused by bbox excedding image boundaries
	for xml_file in os.listdir(IN_ANN):
		tree = ET.parse(os.path.join(IN_ANN,xml_file))  
		root = tree.getroot()
		filename = root[1].text
		bndbox = root.findall('object')
		siize = root.findall('size')
		wd = int(siize[0][0].text)
		ht = int(siize[0][1].text)
		for bb in bndbox:
			if int(bb[4][0].text) < 0:  ##xmin
				print(filename)
				print("Before : " + str(bb[4][0].text))
				bb[4][0].text = '0'
				print("After : " + str(bb[4][0].text))
			if int(bb[4][1].text) < 0:   ##ymin
				print(filename)
				print("Before : " +str(bb[4][1].text))
				bb[4][1].text = '0'
				print("After : " + str(bb[4][1].text))			
			if int(bb[4][2].text) > wd:
				print(filename)
				print("Before : "+str(bb[4][2].text))
				bb[4][2].text = str(wd)
				print("After : " +str(bb[4][2].text))
			if int(bb[4][3].text) > ht:
				print(filename)
				print("Before : "+str(bb[4][3].text))
				bb[4][3].text = str(ht)
				print("After : "+str(bb[4][3].text))

		tree.write(os.path.join(IN_ANN,xml_file))
	print("Done")

def main():
	# change_label_name("Data/annotations/","Gadi","Car")
	# list_all_labels("Data/annotations/")
	# count_of_each_label("Data/annotations/")
	bbox_exceed_image_shape("Data/annotations/")

if __name__ == '__main__':
	main()


