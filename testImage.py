#from fastai.vision.all import *
#from fastcore.all import *
from PIL import Image

imgDir = "images/"
filename = "downloadedCat967.jpg"
dest = imgDir+filename
im = Image.open(dest)
im.to_thumb(256,256)
destNew = imgDir+"2"+filename
im.save(destNew, "JPEG")