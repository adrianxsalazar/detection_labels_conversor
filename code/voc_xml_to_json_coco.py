import os
import argparse
import json
import xml.etree.ElementTree as ET
from typing import Dict, List
from tqdm import tqdm
import re


#Function to obtain information about all the images in the dataset.
def get_images_information(list_all_xml_files):
    #data structures we are going to use.
    id_counter=0

    #the dictionary structure is {filename{filename:,'size':,'width':,'height':}}
    images_information_dictionary={}

    #loop through all the images
    for xml_file in list_all_xml_files:

        #open the xml file.
        ann_tree = ET.parse(xml_file)
        annotation_root = ann_tree.getroot()

        #get the information we need
        filename = annotation_root.findtext('filename')
        img_id = id_counter
        size = annotation_root.find('size')
        width = int(size.findtext('width'))
        height = int(size.findtext('height'))

        image_info_dictionary = {
            'file_name': filename,
            'height': height,
            'width': width,
            'id': img_id}

        #add the image information to out dictionary
        images_information_dictionary[filename]=image_info_dictionary

        #update the id counter
        id_counter=id_counter+1

    return images_information_dictionary


#function to obtain coco information from an object. The information is in
#dictionary shape. The dictionary structure is {'area':,'iscrowd':,'bbox':,
#'category_id':,'ignore':,'segmentation':}
def get_coco_annotation_from_obj(obj, dictionary_clases):
    #get the label
    label = obj.findtext('name')

    #get the id
    category_id = dictionary_clases[label]

    #get information about the bounding box.
    bndbox = obj.find('bndbox')
    xmin = int(bndbox.findtext('xmin')) - 1
    ymin = int(bndbox.findtext('ymin')) - 1
    xmax = int(bndbox.findtext('xmax'))
    ymax = int(bndbox.findtext('ymax'))
    assert xmax > xmin and ymax > ymin, f"Box size error !: (xmin, ymin, xmax, ymax): {xmin, ymin, xmax, ymax}"

    #width and height
    o_width = xmax - xmin
    o_height = ymax - ymin

    #get a dictionary.
    ann = {
        'area': o_width * o_height,
        'iscrowd': 0,
        'bbox': [xmin, ymin, o_width, o_height],
        'category_id': category_id,
        'ignore': 0,
        'segmentation': []  # This script is not for segmentation
    }
    return ann

#function to get a dictionary with the name of the classes and a the id.
def get_dictionary_labels(list_all_xml_files):
    #fempy structures we will use later on.
    class_names=[]
    class_ids=[]
    class_counter=0

    #loop through all the xml files
    for xml_file in list_all_xml_files:
        #parse the xml file
        ann_tree = ET.parse(xml_file)
        ann_root = ann_tree.getroot()

        #Access to the object information
        for obj in ann_root.findall('object'):

            #look for new classes
            if obj.findtext('name') not in class_names:
                class_names.append(obj.findtext('name'))
                class_ids.append(class_counter)
                class_counter=class_counter+1

    #create the dictionary, where the key is the class name and the value the
    #class id.
    dictionary_labels=dict(zip(class_names,class_ids))

    return dictionary_labels

#main function
def main(xml_path,output_path,json_name):

    #get a list of all the xml files in the path
    list_all_xml_files=[os.path.join(xml_path,file) for file in os.listdir(xml_path) if file.endswith('.xml')]

    #get a dictionary to map the names of the class to the class id.
    dictionary_labels=get_dictionary_labels(list_all_xml_files)

    #get a dictionary to map every file to its characteristics
    dictionary_images_information=get_images_information(list_all_xml_files)

    #main dictionary we are goint to populate
    output_json_dict = {
        "images": [],
        "type": "instances",
        "annotations": [],
        "categories": []
    }

    #data structure we are going to use.
    counter_bounding_box=1

    #Loop throught all the xml files. We are aiming to pupulate the json file.
    for xml_file in list_all_xml_files:
        #open xml file
        ann_tree = ET.parse(xml_file)
        annotation_root = ann_tree.getroot()

        #get the filename
        xml_filename=filename = annotation_root.findtext('filename')

        img_info = dictionary_images_information[str(xml_filename)]

        #get the image id
        img_id = img_info['id']

        #update the json file
        output_json_dict['images'].append(img_info)

        #go throught all the objects in the image
        for obj in annotation_root.findall('object'):
            ann = get_coco_annotation_from_obj(obj, dictionary_labels)
            ann.update({'image_id': img_id, 'id': counter_bounding_box})
            print (ann)
            output_json_dict['annotations'].append(ann)
            counter_bounding_box = counter_bounding_box + 1

    #
    for label, label_id in dictionary_labels.items():
        category_info = {'supercategory': 'none', 'id': label_id, 'name': label}
        output_json_dict['categories'].append(category_info)

    #save the json file
    with open(os.path.join(output_path,json_name), 'w') as f:
        output_json = json.dumps(output_json_dict)
        f.write(output_json)





if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='This script support converting voc format xmls to coco format json')

    parser.add_argument('-xml_path', type=str, default=None,
                        help='path to annotation files directory. It is not need when use --ann_paths_list')

    parser.add_argument('-output_path', type=str, default=None,
                        help='')

    parser.add_argument('-json_name', type=str, default=None,
                        help='')

    args = parser.parse_args()

    main(args.xml_path, args.output_path,args.json_name)
