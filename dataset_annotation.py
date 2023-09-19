import os,shutil,re
import cv2
import numpy as np
import pandas as pd

# We will be reading this to concat the dataset to previously annotated dataset
previous_data=pd.read_csv("nails_dataset.csv")

# Reading all the images_name
images_list=[f"{root}/{file}" for root,dir,files in os.walk("curated_dataset") for file in files]

# Structure of the dataset
dataset={
        "image_name":[],
        "length":[],
        "nail_texture":[],
        "moon":[],
        "color":[],
        "bitting":[],
        "nails_side_texture":[]
        }

# details of the dataset
columns_details={
                "image_name":"path of the image",
                "length" : "It shows length of the nails:\n [0]: short \n [1]: Normal \n [2]: Long",
                "nail_texture" : "It shows tecture of nails: \n [0]: Normal \n [1]: BAD \n [2]: Too bad",
                "moon" : "It shows the size of the moon: \n [0]: No moon \n [1]: Little Moon \n [2]: Large Moon",
                "color" : "It represents the color of the Nail \n [r]: Red \n [Y]: [yellow] \n [W]: Whitish \n [P]: Pale \n [C]: Cloudy",
                "bitting" : "It represents bitting of the nail \n [0]: No bitting \n [1]: Bitting",
                "nails_side_texture": "It represents skin texture of nails side \n [0]: Normal \n [1]: BAD \n [2]: Too bad"
                }

# the images which have been annotated will be moved to this directory
os.makedirs("dataset_annoted",exist_ok=True)

def ask_questions(image_path):
    for key,value in columns_details.items():
        state = True
        if key == "image_name":
            dataset["image_name"].append(image_path.split("/")[-1])
        else:
            print(key," : ",value )
            valid_inputs=re.findall(r"\[(.*?)]",value)
            
            while state:
                u_input=input("Enter any option from above:")
                if u_input in valid_inputs:
                    state = False
                else:
                    print("wrong_input")
            dataset[key].append(u_input)

# Dataset annotations on action
for img_path in images_list:
    image=cv2.imread(img_path)
    h,w,_=image.shape
    if h<450 or w < 450:
        image=cv2.resize(image,(450,450))
    else:
        image=cv2.resize(image,(int(w*0.7),int(h*0.7)))
        
    cv2.imshow("image",image)
    ask_questions(img_path)
    cv2.waitKey(0)
    cv2.destroyAllWindows()  

pd.concat([previous_data,pd.DataFrame(dataset)],axis=1)