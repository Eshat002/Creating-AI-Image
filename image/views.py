from django.shortcuts import render
import openai
import os
from dotenv import load_dotenv
import requests
from django.core.files.base import ContentFile
from .models import Image
from django.http import HttpResponse
load_dotenv()

api_key = os.getenv("OPENAI_KEY", None)
openai.api_key = api_key


def create_image_from_text(request):
    obj=None
    if api_key is not None and request.method == "POST":
    
        user_input = request.POST.get("user_input")
        prompt = user_input
        
        try:
            response = openai.Image.create(
            
                prompt=prompt,
                size='256x256'

            )
        
        except Exception as e:
            return HttpResponse("<h1>Given text is not allowed.Please try again with a different text.</h1>")
        
        img_url=response["data"][0]["url"]
        

        response_url=requests.get(img_url)

        img_file=ContentFile(response_url.content)
    
    
        count= Image.objects.all().count() + 1
        fname=f"image-{count}.jpg"
        obj=Image(text=prompt)
        obj.image.save(fname,img_file)
        obj.save()
    

    # else:
    #     return HttpResponse("<h2>Given text is not allowed.Try another text please</h2>")


    return render(request, "home.html", {"obj":obj})
