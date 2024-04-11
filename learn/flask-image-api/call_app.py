import requests
import os
CURR_DIR = os.path.dirname(os.path.realpath(__file__))

endpoint = "http://127.0.0.1:8080"
DATA_IN = f"{CURR_DIR}/data/in"
# r = requests.get(f'{endpoint}/add/2/3')
#
# print(r.content)


def upload_images():
    # Open and read the two images
    with open(f'{DATA_IN}/im1.jpeg', 'rb') as file1, open(f'{DATA_IN}/im2.jpeg', 'rb') as file2:

        files = {'image1': file1, 'image2': file2}

        # Make a POST request to the API with the files
        response = requests.post(f'{endpoint}/merge_images', files=files)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Save the merged image
            with open('merged_image.jpg', 'wb') as merged_image_file:
                merged_image_file.write(response.content)
            print("Merged image saved successfully.")
        else:
            print("Error:", response.json())


upload_images()