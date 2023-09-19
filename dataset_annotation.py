"importing all the libraries"

import os
import shutil
import re
import threading

import cv2
import numpy as np
import pandas as pd

DATASET_PATH = "nails_dataset.csv"

# Reading all the images_name
images_list = [f"{root}/{file}" for root, dir,
               files in os.walk("curated_dataset") for file in files]

# Structure of the dataset
dataset = {
    "image_name": [],
    "length": [],
    "nail_texture": [],
    "moon": [],
    "color": [],
    "bitting": [],
    "nails_side_texture": []
}
# details of the dataset
columns_details = {
    "image_name": "path of the image",
    "length": "It shows length of the nails:\n [0]: short \n [1]: Normal \n [2]: Long",
    "nail_texture": "It shows tecture of nails: \n [0]: Normal \n [1]: BAD \n [2]: Too bad",
    "moon": "It shows the size of the moon: \n [0]: No moon \n [1]: Little Moon \n [2]: Large Moon",
    "color": "It represents the color of the Nail \n [R]: Red \n [Y]: [yellow] \n [W]: Whitish \n [P]: Pale \n [C]: Cloudy",
    "bitting": "It represents bitting of the nail \n [0]: No bitting \n [1]: Bitting",
    "nails_side_texture": "It represents skin texture of nails side \n [0]: Normal \n [1]: BAD \n [2]: Too bad"
}

# We will be reading this to concat the dataset to previously annotated dataset
try:
    previous_data = pd.read_csv(DATASET_PATH, index_col="Unnamed: 0")
except:
    previous_data = pd.DataFrame(dataset)


def ask_questions(image_path: str) -> None:
    """
    this fucntion is used to take user inputs according to the columns in the dataframe.
    """
    for key, value in columns_details.items():
        state = True
        if key == "image_name":
            dataset["image_name"].append(image_path.split("/")[-1])
        else:
            print(key, " : ", value)
            valid_inputs = re.findall(r"\[(.*?)]", value)

            while state:
                u_input = input("Enter any option from above:")
                if u_input in valid_inputs:
                    state = False
                else:
                    print("wrong_input")
            dataset[key].append(u_input)

            # This line of code will automatically clear terminal
            os.system('cls' if os.name == 'nt' else 'clear')

# display of the image


def display_image(img_path: str) -> None:
    """
    This function is responsible for:
     - reading the image and displaying that
     - resizing the image
     - displaying the image
    """
    image = cv2.imread(img_path)
    h, w, _ = image.shape
    if h < 450 or w < 450:
        image = cv2.resize(image, (450, 450))
    else:
        image = cv2.resize(image, (int(w*0.7), int(h*0.7)))

    cv2.imshow(img_path.split("/")[-1], image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# the images which have been annotated will be moved to this directory
os.makedirs("dataset_annotated", exist_ok=True)

# Dataset annotations on action
for img_path in images_list:

    display_thread = threading.Thread(target=display_image, args=(img_path,))
    questions_thread = threading.Thread(target=ask_questions, args=(img_path,))

    display_thread.start()
    questions_thread.start()

    questions_thread.join()
    print(
        f"Sucessfully recorded data, Now drop the image for updating this to : {DATASET_PATH}")
    display_thread.join()

    # Moving the annotated image to another folder named "dataset_annotated"
    dest_dir = os.path.join(
        "dataset_annotated", img_path.split("/")[-1])
    shutil.move(img_path, dest_dir)
    print(f"successfully moved the image to {dest_dir}")

    # Saving the Updated dataset back to csv file
    pd.concat([previous_data, pd.DataFrame(dataset)],
              ignore_index=True).to_csv(DATASET_PATH)

    print(f"succesfully updated csv file: { DATASET_PATH }")
