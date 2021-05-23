from django.shortcuts import render


# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .apps import FastbertConfig
import io
from io import BytesIO
import requests
import tensorflow as tf
from tensorflow import keras
import os
import tempfile


from matplotlib import pyplot as plt
import numpy as np
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import pickle
import requests
from bs4 import BeautifulSoup
import json

decoded = {}
def preprocess_image(image):
	image = tf.image.resize_with_crop_or_pad(image, 224,224)
	return image


@csrf_exempt   
def imagedef(request):
	if request.method == 'POST':
	
		# img_data = request.body
		img_data = (request.body)
		
		
		img = Image.frombytes("RGB",(224,224), img_data,"raw")
		# print(img)
		# img = pickle.loads(img_data)
		img = np.array(img)
		# print(img.shape)
		img = preprocess_image(img)
		x = tf.keras.preprocessing.image.img_to_array(img)
		x = tf.keras.applications.mobilenet.preprocess_input(
    	x[tf.newaxis,...])
		labels_path = "/home/caprize/AIdata/archive/meta/meta/labels.txt"
		imagenet_labels = np.array(open(labels_path).read().splitlines())

		result_before_save = FastbertConfig.model(x)

		decoded = imagenet_labels[np.argsort(result_before_save)[0,::-1][:5]]
		ans = ''
		g=0
		for i in decoded:
			ans+=i
			g+=1
			if (g!=5):
				ans+=" "
		print(ans)
		return HttpResponse(ans)
		        
		# returning JSON response
	if request.method == 'GET':
            
		return JsonResponse(decoded)

@csrf_exempt   
def recipedef(request):
	if request.method == 'POST':
		# img_name = str(request.FILES['dish'].read())
		img_name = str(request.body)
		print(img_name)
		img_name = img_name[2:-1]
		print(img_name)
		user_id = 12345
		url = 'https://www.allrecipes.com/recipe/'+img_name+'/' # url для второй страницы


		recipe_page = requests.get(url)
		recipe_page = str(recipe_page.text)
		recipe_page = BeautifulSoup(recipe_page, "lxml")
		table_i = recipe_page.findAll('span', class_='ingredients-item-name')
		ingredients={}
		n=0
		for i in table_i:
			n+=1
			j = str(i.text)
			# print(j)
			# j = j[36::]
			# k = "</span>"
			# a = j.find(k)
			# print(i)
			ingredients.update({str(n)+".":j[0:len(j)-1]})
		table_s = recipe_page.findAll('div', class_='paragraph')
		n=0
		for i in table_s:
			n+=1
			j = str(i.text)
			print(j)
			ingredients.update({str(n)+")":j[0:len(j)-1]})
		ans = json.dumps(ingredients)
		print(ans)
		return JsonResponse(ans,safe=False)
				        
				# returning JSON response
	if request.method == 'GET':
            
		return JsonResponse(decoded)


@csrf_exempt   
def dish_imagedef(request):
	if request.method == 'POST':
		img_name = str((request.body))
		img_name = img_name[2:-1]
		path = '/home/caprize/AIdata/archive/images/' + img_name +"/"
		fnames = os.listdir(path)
		ans_path = '/home/caprize/AIdata/archive/images/' + img_name +"/"+fnames[0]
		with open(ans_path, "rb") as f:
			ans = f.read()
			f.close()
		return HttpResponse(ans)
		
				        
				# returning JSON response
	if request.method == 'GET':
            
		return JsonResponse(decoded)
