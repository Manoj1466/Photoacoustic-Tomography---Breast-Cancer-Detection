from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
import pymysql
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import matplotlib.pyplot as plt
import re
import cv2
import numpy as np
import os
import tensorflow as tf
from keras.models import model_from_json
from keras.applications.mobilenet_v2 import preprocess_input
from PIL import Image
from io import BytesIO
from keras.preprocessing.image import img_to_array

global model   


def load_request_image(image):
    image = Image.open(BytesIO(image))
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize((48, 48))
    image = img_to_array(image)
    image = preprocess_input(image)
    image = np.expand_dims(image, axis=0)

    return image
   

def predict_class(image_array):
    json_file = open('./model/model.json', 'r')
    model_json = json_file.read()
    json_file.close()
    model = model_from_json(model_json)
    model.load_weights("./model/weights.h5")
    classes = ["Benign", "Malignant"]
    y_pred = model.predict(image_array)
    class_index = np.argmax(y_pred, axis=1)  # Use axis=1 to get the index for each example in the batch
    confidence = y_pred[0][class_index[0]]  # Extract the confidence for the predicted class
    class_predicted = classes[class_index[0]]  # Assuming batch size is 1
    
    return class_predicted, confidence

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})

def Uploadimage(request):
    if request.method == 'GET':
        return render(request, 'Uploadimage.html', {})
        
def Result(request):
    if request.method == 'GET':
        return render(request, 'Result.html', {})

  

def UserLogin(request):
    if request.method == 'POST':
      username = request.POST.get('username', False)
      password = request.POST.get('password', False)
      index = 0
      con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'BreastCancer',charset='utf8')
      with con:    
          cur = con.cursor()
          cur.execute("select * FROM users")
          rows = cur.fetchall()
          for row in rows: 
             if row[0] == username and password == row[1]:
                index = 1
                break		
      if index == 1:
       file = open('session.txt','w')
       file.write(username)
       file.close()   
       context= {'data':'welcome '+username}
       return render(request, 'UserScreen.html', context)
      else:
       context= {'data':'login failed'}
       return render(request, 'Login.html', context)

def Signup(request):
    if request.method == 'POST':
      username = request.POST.get('username', False)
      password = request.POST.get('password', False)
      contact = request.POST.get('contact', False)
      email = request.POST.get('email', False)
      address = request.POST.get('address', False)
      db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'BreastCancer',charset='utf8')
      db_cursor = db_connection.cursor()
      student_sql_query = "INSERT INTO users(username,password,contact_no,email,address) VALUES('"+username+"','"+password+"','"+contact+"','"+email+"','"+address+"')"
      db_cursor.execute(student_sql_query)
      db_connection.commit()
      print(db_cursor.rowcount, "Record Inserted")
      if db_cursor.rowcount == 1:
       context= {'data':'Signup Process Completed'}
       return render(request, 'Register.html', context)
      else:
       context= {'data':'Error in signup process'}
       return render(request, 'Register.html', context)

def UploadimageAction(request):
    if request.method == 'POST' and 't1' in request.FILES:
        image = request.FILES['t1'].read()
        image = load_request_image(image)
        class_predicted, confidence = predict_class(image)
        output = '<table border=1 align=center><tr><th>Result</th><th>Accuracy Score</th></tr>'
        output+='<tr><td><font size="" color="white">'+class_predicted+'</td><td><font size="" color="white">'+str(confidence)+'</td></tr>'
        context= {'data':output}
        return render(request,'Result.html',context)
    else:
        return HttpResponse(request,'Uploadimage.html',{})
