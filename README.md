# An Interactive Web Application for Reducing Toxic Exposures in Homes
In this project, we partnered with Alan Kadish from Pure Living. Pure Living is a company that strives to help people live a less toxic lifestyle. Pure Living wanted a web application that allows the user to evaluate the contents of their home to determine what items may be unknowingly toxic to human health and provide the user with safer alternatives. As a starting point for this project, Alan wanted us to begin with evaluating the contents found in a typical bedroom, and then later iterations of this project could build on what we built and add additional rooms and objects for the program to evaluate.  

To achieve this goal, our project utilizes cutting-edge object detection technology and 3D imaging software to allow users the ability to assess the contents of their homes. We have given users two ways to interact with this project in hopes that it will encourage more people to use the program and so that more people will be educated on the potential risks in their homes and how to avoid those risks.

Users have two options to use this program. They can either upload an image of their own room to be analyzed or they can view a pre-loaded 3D model.

### Object Detection
To accomplish this task, we used a custom trained image detection model that detects eighteen common household items that are toxic to human health.  Once the user uploads their picture, the image is run through the custom trained image detection model and then the program displays the picture with the objects detected and provides the user with a brief description of each object detected and why it may be toxic to their health.  

### [3D Model](https://cdominitz.github.io/Capstone-Project/templates/model)
When a user selects the option to view a 3D model room, they navigate to a page that is preloaded with a model that the user is able to explore. They can zoom in and out as well as change the direction of viewing the room. Anytime the user clicks on an object, they are shown a description about the object that was clicked as well as any relevant links to learn more information. 

## Installation and Instruction
1. To clone the Github repository to your local machine, in the terminal navigate to the path of the directory where you want to clone the repo and run the following command in the terminal:

    git clone "https://github.com/cdominitz/capstone-project.git"

2. From the terminal, navigate to the capstone-project directory

3. To install the libraries and packages needed to run this project, run the following command in the terminal:

    pip install -r requirements.txt

4.  After the libraries and packages have been installed, run the following command in the terminal:

    python main.py

The app will begin to run and you can access it at http://127.0.0.1:5000

### Additional Notes:
It is a good idea to set up a virtual environment to run steps 3 and 4 in so that none of the packages in requirements.txt change anything on your system that other programs you have may depend on.  When you set up your virtual environment use Python 3.9.18 in the virtual environment. 
 
As you play around with the application and upload pictures, please note that the pictures you upload will be saved to the uploads directory located inside the static directory.  Each time an image is run through the image detection model it saves the image with the detected objects to a predict directory inside runs/detect.  It is a good idea to delete the images located in the uploads directory and all the predict folders once you are done experimenting with the application.  DO NOT DELETE the uploads directory or else you will be unable to upload images anymore. 

For changing the model that is used for this web application, babylon.js supports files .obj, .gltf (.glb), .stl, and .babylon. Any models in these formats should be able to be put in place of the current file ‘another_bedroom.glb’ as long as the file name and path are updated in scripts.js. If the object information dictionary for the model needs to be updated, replace or update the current csv and run ‘create_json.js > infoDict.js’ or update the dictionary in ‘infoDict.js’.

The 3D model also uses the cdn from babylon.js. When this app is ready for public deployment, this will require to be run on your own CDN in order to have a more efficient and seamless product.
