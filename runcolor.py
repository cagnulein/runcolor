from PIL import Image
import re
import requests
from bs4 import BeautifulSoup
import numpy as np
import argparse
import cv2
import os
import sys

OUTPUT_FOLDER = "/tmp/"
s = 1 # for example sensitivity=5/256 color values in range [0,255]
PIXEL_NUMBER = 2000 #numero di pixel con il colore selezionato

#seleziona un colore per il quale vuoi cercare, di default giallo
boundaries = [
#([17, 15, 100], [50, 56, 200]),  #rosso
#([86, 31, 4], [220, 88, 50]),    #blu
([25, 146, 190], [62, 174, 250]), #giallo
#([103, 86, 65], [145, 133, 128]) #grigio
]


def color(file):
    image = cv2.imread(file)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    boundaries = [([25, 146, 190], [62, 174, 250])]

    for i, (lower, upper) in enumerate(boundaries):
       lower = np.array([color-s if color-s>-1 else 0 for color in lower], dtype="uint8")
       upper = np.array([color+s if color+s<256 else 255 for color in upper], dtype="uint8")
       mask = cv2.inRange(image, lower, upper)
    n_pix = np.sum(mask == 255)
    #print(n_pix)
    return n_pix

#site = 'http://www.reggiocorre.it/showg.aspx?aid=10659'

response = requests.get(sys.argv[1])

soup = BeautifulSoup(response.text, 'html.parser')
img_tags = soup.find_all('img')
urls = [img['src'] for img in img_tags]

for url in urls:
    filename = re.search(r'/([\w_-]+[.](jpg|gif|png|JPG|GIF|PNG))$', url)
    with open(OUTPUT_FOLDER + filename.group(1), 'wb') as f:
        if 'http' not in url:
        # sometimes an image source can be relative 
        # if it is provide the base url which also happens 
        # to be the site variable atm. 
            url = '{}{}'.format("http://www.reggiocorre.it/", url)
        response = requests.get(url)
        f.write(response.content)
        #not matching
        if(color(OUTPUT_FOLDER + filename.group(1)) < PIXEL_NUMBER):
            os.remove(OUTPUT_FOLDER + filename.group(1))
        else:
            print(filename.group(1))
            #print(url)
