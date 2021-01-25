These are several pythons file to transform popular object detection annotation
formats such as COCO Json, VOC xml or Darknet. So the labelling format will not be
a limitation in our experiments.

The python files in this repo can convert

<ul>
 <li>COCO Json to VOC xml.</li>
 <li>COCO Json to Darknet.</li>
 <li>VOC xml to COCO Sjon.</li>
</ul>

We use COCO Json as a central detection annotation format. We provide tools to
transform the detection annotation formats to COCO Json. Then, you will be able
to convert the COCO Json file into any format.

Running the file is simple. You have to use the commands to indicate the location
of the detection annotation files and the path of the folder where you have the
images. Below, you can find some examples of the commands to run the conversors.

The following command takes a COCO ".json" file called "dataset.json" and transforms it into several darknet
files, which the code saves in the same path as the images, which in this case is "./dataset/images/". The parameter "-json_path"
indicates the path of the COCO ".json" file and the parameter "-image_path" shows the
path that contains the data/images.

```

$ python code/coco_json_to_darknet.py -json_path "dataset.json" -image_path "./dataset/images/"

```

This other command takes a gets all the VOC xml file in the path "./dataset/images/"
file and transforms it into several darknet
files, which the code saves in the same path as the images. The parameter "-json_path"
indicates the path of the COCO ".json" file and the parameter "-image_path" shows the
path that contains the data/images.

```

$ python code/coco_json_to_darknet.py -json_path "" -image_path ""

```


<h3> Parameters for coco_json_to_voc_xml.py </h3>

```

-> -model: description=standard model used for training,
            required=False, default="COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml", type=str

-> -check_model: description=check if there is a checkpoint from previous trainings processes,
            required=False, default=False, type=bool

-> -model_output: description=where the model is going be stored,
            required=False, default="dataset_A", type=str

-> -dataset: description=dataset to use,
            required=False, default="dataset_A", type=str

-> -standard_anchors: description=True if we want to use the standard anchor sizes, False if we want to suggest ours,
            required=False, default=True, type=bool

-> -learning_rate: description=learning rate in the training process
            required=False, default=0.0025, type=float

-> -images_per_batch: description=number of images used in each batch,
            required=False, default=6, type=int

-> -anchor_size: description= if -standard_anchors is True, the size of the anchors in the rpn,
            required=False, default='32,64,128,256,512', type=str

-> -aspect_ratios: description= if -standard_anchors is True, this indicates the aspect ration to use in the rpn
            required=False, default='0.5,1.0,2.0', type=str )

-> -roi_thresh: description=Overlap required between a ROI and ground-truth box in order for that ROI to be used as training example,
            required=False, default=0.5, type=float

-> -number_classes: description=number of classes,
            required=False, default=1, type=int

-> -evaluation_period: description= The command indicates the number of epochs required to evaluate our model in the validations set,
            required=False, default=5, type=int)

-> -patience: description= Number of evaluations without improvement required to stop the training process,
            required=False, default=20, type=int

-> -warm_up_patience: description=Number of evaluations that will happen independently of whether the validation loss improves,
            required=False, default=20, type=int


```

<h3> Parameters for voc_xml_to_json_coco.py</h3>




<h3> Parameters for coco_json_to_darknet.py</h3>
