import os
import json
from os import listdir, getcwd
from os.path import join
import argparse

#Function to obtain the relative bounding box coordinates.
def yolo_convert_bounding_box(image_width,image_height,box):
    dw = 1./image_width
    dh = 1./image_height
    x = box[0]*dw
    y = box[1]*dh
    w = box[2]*dw
    h = box[3]*dh
    return (x,y,w,h)

#main function to transform the COCO json to darknet.
def main(json_path,image_path):
    with open(json_path,'r') as f:
        data = json.load(f)

    for item in data['images']:
        #get basic information of the image
        image_id = item['id']
        file_name = item['file_name']
        width = item['width']
        height = item['height']

        #return the annotations(bounding boxes with the same image id as the image)
        value = filter(lambda item1: item1['image_id'] == image_id,data['annotations'])

        name,extension = os.path.splitext(file_name)

        txt_file_name=os.path.join(image_path,name+".txt")

        outfile = open(txt_file_name, 'a+')

        #go through all the bounding boxes linked with the image.
        for bounding_box in value:

            #get the category id of the bounding box
            category_id = bounding_box['category_id']

            #Get the coordinates of the bounding box
            box = bounding_box['bbox']

            bb = yolo_convert_bounding_box(width,height,box)

            #
            outfile.write(str(category_id)+" "+" ".join([str(a) for a in bb]) + '\n')

        outfile.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='This script support converting voc format xmls to coco format json')

    parser.add_argument('-json_path', type=str, default=None,
                        help='path to annotation files directory. It is not need when use --ann_paths_list')

    parser.add_argument('-image_path', type=str, default=None,
                        help='')

    args = parser.parse_args()

    main(args.json_path, args.image_path)
