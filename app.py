from fastai.vision.all import *
from flask import Flask
app = Flask(__name__)

import json
from flask import request
import os
import time
from PIL import Image

from os import listdir
from os.path import isfile, join

from fastcore.all import *
from fastdownload import download_url

# obj = dict(error = False, isCat = None)

import __main__
def is_cat(x): return x[0].isupper() 
__main__.is_cat = is_cat

learn = load_learner('model.pkl')

@app.route("/", methods=['GET', 'POST'])
def hello():
    obj = {
        "error": False,
        "message": None,
        "isCat": None
        }

    # handle the POST request
    if request.method == 'POST':
        #url = request.form.get('imageLink')

        # Get the JSON payload from the request body
        data = request.get_json()
        # Decode the URL
        decoded_url = urllib.parse.unquote(data['imageLink'])

        randomInt = random.randint(10, 1000)
        imgDir = "images/"
        catDir = "static/catImages/"
        otherDir = "static/otherImages/"
        filename = f"downloadedCat{randomInt}.jpg"
        dest = imgDir+filename
        destNew = imgDir+"2"+filename
        destCat = catDir+filename
        destOther = otherDir+filename
        try:
            download_url(decoded_url, dest, show_progress=False)
        except:
            obj["error"] = True
            obj["message"] = "Download error: This picture does not work.  Try a different one. "+decoded_url
            return obj
        time.sleep(1)
        try:
            im = Image.open(dest)
            im.to_thumb(256,256)
            im.save(destNew, "JPEG")
        except:
            obj["error"] = True
            obj["message"] = "Error saving image: This picture does not work.  Try a different one."
            os.remove(dest)
            os.remove(destNew)
            return obj

        os.remove(dest)
        try:
            is_cat,_,probs = learn.predict(destNew)
        except:
            obj["error"] = True
            obj["message"] = "Predict error: This picture does not work.  Try a different one."
            os.remove(dest)
            os.remove(destNew)
            return obj
        
        obj["isCat"] = is_cat

        if is_cat == 'True':
            os.rename(destNew, destCat)
        else:
            os.rename(destNew, destOther)

        obj["yourImage"] = destCat

        catfiles = [f for f in listdir(catDir) if isfile(join(catDir, f))]
        catfiles = ["catImages/" + f for f in catfiles]
        obj["catImages"] = catfiles

        otherfiles = [f for f in listdir(otherDir) if isfile(join(otherDir, f))]
        otherfiles = ["otherImages/" + f for f in otherfiles]
        obj["otherImages"] = otherfiles

        
        return obj

    # otherwise handle the GET request
    obj["error"] = True
    obj["message"] = 'isCat requires POST method.  You have made GET request'
    return obj
