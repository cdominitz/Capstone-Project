from flask import Flask, flash, redirect, render_template, request, session
import os
from werkzeug.utils import secure_filename
from ultralytics import YOLO
import cv2
 
# Defining upload folder path
UPLOAD_FOLDER = os.path.join('static', 'uploads')
# Define allowed files
ALLOWED_EXTENSIONS = {'jpg'}
 
app = Flask(__name__)

# Configure upload folder for Flask application
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 
# Define secret key to enable session
app.secret_key = 'cs467'

# Define dictionary containing the toxic items to be detected and their descriptions
object_descriptions = {"Candle": "For more information, visit pureliving.com",
    "Clock": "For more information, visit pureliving.com", 
    "Television": "Did you know that many brands of televisions outgas volatile organic compounds (VOC’s) chemicals ? Think of the new smell which is typically from flame retardants, deca-BDE and DBDPE found in the plastic casing. Apparently, the usual manufacturers are not providing adequate information to know which to choose as evidenced by the repeated requests from multiple organizations. The best alternative, keep the television out of your bedroom. For more information as it becomes available go to PureLiving.com ", 
    "Mirror": "For more information, visit pureliving.com", 
    "Cat": "For more information, visit pureliving.com", 
    "Bookcase": "For more information, visit pureliving.com", 
    "Bed": "For your headboard and footboard, the safest way to go is powder coated metal or real wood sealed with safe stains and coatings. Painted products should be suspect. You can tell the difference between painted vs powder coating by using a penny to scrape the surface in an area not generally seen. Paint will scratch off easily vs powder coated surfaces which are much harder to remove. Mattresses come in many formats from the common coil and cloth to the various foams, and combinations. The key is to know the composition, is the foam petrochemical or natural, has there been any treatments to the fabrics and are they organic. Check the labels on the products and look for both the GOTS (Global Organic Trade Standard) certification, as one example of and ideal product. Remember there are many trade certifications that are meaningless, so look for more information on PureLiving.com.   ", 
    "Curtain": "Think about the fabrics, are they organic, using non-toxic dyes and you can see where this is headed. Check the labels and avoid products that are stain resistance. Most washing labels will contain some information on composition of the products. Blinds come in a variety of materials from real wood to plastics and metal. With the inexpensive plastic blinds, you’ll typically find them made of PVC not an ideal material in your home as they contain endocrine disruptors and chlorinated chemicals.", 
    "Makeup": "For more information, visit pureliving.com", 
    "Perfume": "For more information, visit pureliving.com", 
    "Chest of drawers": "Chest of drawers are made with so many materials it’s important to open the draws and check all surfaces. Commonly made particle board and or carboard construction is generally not a healthy option. Remember to also consider the surface treatments as they are significant.", 
    "Lamp":"Curiously most of the shades are made with PVC which has no business in your bedroom. An obvious change is making certain your using LED bulbs as they produce far less hot reducing your exposure to the outgassing. ",
    "Chair":"As most chairs incorporate petrochemical foams and may be constructed using plastic or fabric coverings. You’ll commonly find an attached label that will tell you if the products been treated with fire proofing agents. Avoid these and keep on looking for a better option. The surface treatments are commonly using forever chemicals for waterproofing and stain resistance, both are not healthy options. Don’t forget the ergonomics of the chair by seeing our Pure Living page. ", 
    "Dog":"For more information, visit pureliving.com", 
    "Desk":"When considering most desks if the construction is wood, consider if it’s, real or manufactured wood. If your desk is metal construction check if its painted or powder coated.  Then check the surfaces for stains and paints and other coatings. And don’t forget the ergonomics of your setup. See the Pure Living page for more information.  ", 
    "Nightstand":"The key when considering most nightstands is the construction, real or manufactured woods, stains and surface treatments, including painted surfaces. Ideally the nightstand should be all real wood and coated with safe treatments. Check the labels for fire retardants and choose other options.", 
    "Window":"For more information, visit pureliving.com", 
    "Closet":"For more information, visit pureliving.com", 
    "Flooring":"Flooring is one of the most complex systems. The subfloor and the actual flooring surface can be a combination of particle board, different types of plywood, or even concrete. What we place as the finished surface includes, vinyl, ceramic, carpet, real and engineered wood and more. Each has its benefits and drawbacks. One consideration is when was the product purchased. As a consumer you’ll notice the big brand stores have recently, last few years, reduced the amount of formaldehyde and other chemicals in their products."}

def detection(img_path, img_filename):
    '''This function loads the custom trained image detection model, runs the user's image through the dection, then
    returns the path of the output image with detections along with a list of the names of the objects detected in the image'''
    # Load the custom trained image detection model
    model = YOLO('CustomModel.pt')
    names = model.names 
    # Run the image through the image detection model
    results = model.predict(source=img_path, conf=0.25, save=True, show_conf=False)

    # Get the class names for each object detected in the image
    class_names = []
    for result in results:
        for object in result.boxes.cls:
            class_names.append(names[int(object)])

    # Find the path to the image that was most recently run through the image detection model:
    detect_dir_path = os.path.join('runs', 'detect')
    all_subdirs = os.listdir(detect_dir_path)
    latest_predict = max(all_subdirs, key=lambda d: os.path.getmtime(os.path.join(detect_dir_path, d)))
    img_detect_file_path = os.path.join('runs', 'detect', latest_predict, img_filename)

    class_names = set(class_names) # Remove duplicates from class_names
    return img_detect_file_path, list(class_names)

def move_detection_image(img_detect_file_path, img_file_path, filename):
    '''This function moves the output image with the detections generated in the detection function to static/uploads so that it can be 
    rendered on the screen'''
    img = cv2.imread(img_detect_file_path)
    os.chdir(img_file_path)
    cv2.imwrite(filename, img)
    os.chdir('..')
    os.chdir('..')
    return
 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/model')
def model():
    return render_template('model.html')

@app.route('/index1')
def index1():
    return render_template('index1.html')
 
@app.route('/',  methods=("GET","POST" ))
def upload_file():
    # This function was adapted from https://flask.palletsprojects.com/en/2.3.x/patterns/fileuploads/
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        # Upload file
        file = request.files['file']
        # If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # If the user did upload a file, extract the file name and save the image
        img_filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        # Store the path of the uploaded image and run the it through the image detection model
        img_file_path = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
        img_detect_file_path, detected_objects = detection(img_file_path, img_filename)
        move_detection_image(img_detect_file_path, app.config['UPLOAD_FOLDER'], img_filename)
        session['detected_img_file_path']= os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
        session['detected_objects'] = detected_objects
        return render_template('index2.html')
 
@app.route('/show_image')
def displayImage():
    # Get the path to the image that has gone through the image detection and a list of the detected objects in the image
    img_file_path = session.get('detected_img_file_path', None)
    detected_objects = session.get('detected_objects', None)
    # Display image with the detected objects and their descriptions
    return render_template('show_image.html', detected_image = img_file_path, detected_objects = detected_objects, object_descriptions = object_descriptions)
 
if __name__=='__main__':
    app.run(debug = True)
