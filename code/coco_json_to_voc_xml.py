import os
import xml.etree.ElementTree as ET
import pandas as pd
import cv2
import json
import argparse
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def generate_xml_template():
    annotation = Element('annotation')

    #subelements
    folder = SubElement(annotation, 'folder')
    filename = SubElement(annotation, 'filename')
    path = SubElement(annotation, 'path')
    source = SubElement(annotation, 'source')
    size = SubElement(annotation, 'size')
    segmented = SubElement(annotation, 'segmented')

    #subsubelements
    database = SubElement(source, 'database')
    width = SubElement(size, 'width')
    height = SubElement(size, 'height')
    depth = SubElement(size, 'depth')

    #text
    database.text = 'Unknown'

    return annotation

def write_to_xml(image_name, image_dictionary, image_path):
    # get bboxes
    bounding_boxes = image_dictionary[image_name]

    # read xml file
    root = generate_xml_template()

    # modify
    folder = root.find('folder')
    folder.text = 'all'

    #
    fname = root.find('filename')
    fname.text = image_name

    #size
    img = cv2.imread(os.path.join(image_path, image_name))
    h,w,d = img.shape
    #
    size = root.find('size')
    width = size.find('width')
    width.text = str(w)
    height = size.find('height')
    height.text = str(h)
    depth = size.find('depth')
    depth.text = str(d)


    for box in bounding_boxes:
        # append object
        obj = ET.SubElement(root, 'object')

        #
        name = ET.SubElement(obj, 'name')
        name.text = box[0]

        #
        pose = ET.SubElement(obj, 'pose')
        pose.text = 'Unspecified'

        truncated = ET.SubElement(obj, 'truncated')
        truncated.text = str(0)

        difficult = ET.SubElement(obj, 'difficult')
        difficult.text = str(0)

        bndbox = ET.SubElement(obj, 'bndbox')

        xmin = ET.SubElement(bndbox, 'xmin')
        xmin.text = str(int(box[1]))

        ymin = ET.SubElement(bndbox, 'ymin')
        ymin.text = str(int(box[2]))

        xmax = ET.SubElement(bndbox, 'xmax')
        xmax.text = str(int(box[3]))

        ymax = ET.SubElement(bndbox, 'ymax')
        ymax.text = str(int(box[4]))

    # save xml element.
    print (image_name)
    #get the name and the extension of our file
    name, extension = os.path.splitext(image_name)
    xml_file_name=os.path.join(image_path,name+".xml")

    #print  prettify(root)
    tree = ET.ElementTree(root)
    tree.write(xml_file_name)


#Function to create a dictionary that will allow us to get the class name from
#the class id.
def dictionary_id_image_to_image_name(json_path):
    with open(json_path,'r') as f:
        data = json.load(f)

    #Empty data structures we will use.
    dict_id_image_image_name={}

    for item_image in data["images"]:
        dict_id_image_image_name[item_image["id"]]=item_image["file_name"]

    return dict_id_image_image_name


#Function to create a dictionary that will allow us to get the class name from
#the class id.
def dictionary_id_class_to_class_name(json_path):
    with open(json_path,'r') as f:
        data = json.load(f)

    #Empty data structures we will use.
    dict_id_class_name={}

    for item_class in data['categories']:
        dict_id_class_name[item_class["id"]]=item_class["name"]

    return dict_id_class_name

def main(json_path, image_path):
    # read annotations file
    dict_id_class_name=dictionary_id_class_to_class_name(json_path)

    dict_id_image_image_name=dictionary_id_image_to_image_name(json_path)

    # read the COCO json file
    with open(json_path,'r') as f:
        data = json.load(f)

    # get annotations
    annotations = data['annotations']

    #iscrowd allowed character
    iscrowd_allowed = 0

    #dictionary to store the information for each image. The format of the
    #dictionary is {image_name:[[category_bb,xmin,ymin,xmax,ymax],[],....]}
    image_dictionary = {}

    # loop through the annotations in the subset
    for bounding_box in annotations:
        # get annotation for image name.
        image_id = bounding_box['image_id']
        image_name = dict_id_image_image_name[image_id]

        #get the name of the class.
        category = dict_id_class_name[bounding_box['category_id']]

        # append bounding boxes to it
        box = bounding_box['bbox']

        #add as a key to image_dict
        if image_name not in image_dictionary.keys():
            image_dictionary[image_name]=[]

        #since bboxes = [xmin, ymin, width, height]:
        image_dictionary[image_name].append([category, box[0], box[1], box[0]+box[2], box[1]+box[3]])

    # generate .xml files
    for image_name in image_dictionary.keys():
        write_to_xml(image_name, image_dictionary, image_path)
    #     print('generated for: ', image_name)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='This script support converting voc format xmls to coco format json')

    parser.add_argument('-json_path', type=str, default=None,
                        help='path to annotation files directory. It is not need when use --ann_paths_list')

    parser.add_argument('-image_path', type=str, default=None,
                        help='')

    args = parser.parse_args()

    main(args.json_path, args.image_path)
