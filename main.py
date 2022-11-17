import joblib
import string
import cv2
import numpy as np
filename = 'trainedModel.joblib'
model = joblib.load(filename)
from flask import Flask
from io import BytesIO
import boto3
import base64
from flask import request
import random
from captcha.image import ImageCaptcha

app = Flask(__name__)

@app.route('/captcha', methods=['GET', 'POST'])
def captchaResult():

   capt=''
   if request.method == 'POST':
       data = request.data
       imgdata = base64.b64decode(data)
       imgdata = np.asarray(bytearray(imgdata), dtype="uint8")
       img = cv2.imdecode(imgdata, cv2.IMREAD_GRAYSCALE)
       if img is None:
           print("Not detected")
       else:
           img = img / 255.0
           res = np.array(model.predict(img[np.newaxis, :, :, np.newaxis]))
           ans = np.reshape(res, (5, 36))
           l_ind = []
           probs = []
           for a in ans:
               l_ind.append(np.argmax(a))
               probs.append(np.max(a))
           symbols = string.ascii_lowercase + "0123456789" # All symbols captcha can contain
           capt = ''
           for l in l_ind:
               capt += symbols[l]

   return str(capt)

@app.route('/captchaGenerate', methods=['GET', 'POST'])
def main():
    alpha = []
    ALPHA=[]
    num=[]
    for i in range(65,91):
        ALPHA.append(chr(i))
        alpha.append(chr(i).lower())
    for i in range(0,10):
        num.append(i)
    s_alpha = random.choice(alpha)
    c_alpha = random.choice(ALPHA)
    c_alpha1 = random.choice(ALPHA)
    num1 = random.choice(num)
    num2 = random.choice(num)
    num3 = random.choice(num)
    row_captcha = s_alpha+str(num3)+c_alpha+str(num2)+c_alpha1+str(num1)
    row_captcha = list(row_captcha)
    random.shuffle(row_captcha)
    row_captcha = ''.join(row_captcha)
    img = ImageCaptcha()
    image = img.generate_image(row_captcha)
    image.show()
    return row_captcha

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1234, debug=True)
