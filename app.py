from fastai.vision.all import *
from flask import Flask
app = Flask(__name__)

import json
from flask import request
import os
import time
from PIL import Image

from fastcore.all import *
from fastdownload import download_url

obj = {
  "error": False,
  "message": None,
  "isCat": None
}

# obj = dict(error = False, isCat = None)

import __main__
def is_cat(x): return x[0].isupper() 
__main__.is_cat = is_cat

learn = load_learner('model.pkl')

@app.route("/", methods=['GET', 'POST'])
def hello():
    # handle the POST request
    if request.method == 'POST':
        url = request.form.get('imageLink')
        randomInt = random.randint(10, 1000)
        imgDir = "images/"
        catDir = "catImages/"
        otherDir = "otherImages/"
        filename = f"downloadedCat{randomInt}.jpg"
        dest = imgDir+filename
        destNew = imgDir+"2"+filename
        destCat = catDir+filename
        destOther = otherDir+filename
        download_url(url, dest, show_progress=False)
        #time.sleep(1)
        try:
            im = Image.open(dest)
            im.to_thumb(256,256)
            im.save(destNew, "JPEG")
        except:
            obj["error"] = True
            obj["message"] = "This picture does not work.  Try a different one."
            os.remove(dest)
            os.remove(destNew)
            return obj

        os.remove(dest)
        try:
            is_cat,_,probs = learn.predict(destNew)
        except:
            obj["error"] = True
            obj["message"] = "This picture does not work.  Try a different one."
            os.remove(dest)
            os.remove(destNew)
            return obj
        
        obj["isCat"] = is_cat

        if is_cat == 'True':
            os.rename(destNew, destCat)
        else:
            os.rename(destNew, destOther)

        return obj

    # otherwise handle the GET request
    obj["error"] = True
    obj["message"] = 'isCat requires POST method.  You have made GET request'
    return obj
