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

# url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/3-Colored_Norwegian_Forest_Cat.jpg/800px-3-Colored_Norwegian_Forest_Cat.jpg'
# dest = 'downloadedCat01.jpg'
# download_url(url, dest, show_progress=False)
# im = Image.open(dest)
# im.to_thumb(256,256)
# im.save("thumb"+ dest, "JPEG")
learn = load_learner('model.pkl')
# is_cat,_,probs = learn.predict(dest)
# obj["isCat"] = is_cat


@app.route("/", methods=['GET', 'POST'])
def hello():
    # handle the POST request
    if request.method == 'POST':
        url = request.form.get('imageLink')
        randomInt = random.randint(10, 1000)
        imgDir = "images/"
        filename = f"downloadedCat{randomInt}.jpg"
        dest = imgDir+filename
        download_url(url, dest, show_progress=False)
        #time.sleep(1)
        im = Image.open(dest)
        im.to_thumb(256,256)
        destNew = imgDir+"2"+filename
        im.save(destNew, "JPEG")
        os.remove(dest)
        try:
            is_cat,_,probs = learn.predict(destNew)
        except:
            obj["error"] = True
            obj["message"] = "This picture does not work.  Try a different one."
        obj["isCat"] = is_cat
        return obj

    # otherwise handle the GET request
    obj["error"] = True
    obj["message"] = 'isCat requires POST method.  You have made GET request'
    return obj
#    return f"Is a cat?: {is_cat}. \n"


# if __name__ == '__main__':
#     app.run(debug=True)

# print(f"Is a cat?: {is_cat}.")
# print(f"Probability it's a cat: {probs[0]}")

# print("done")