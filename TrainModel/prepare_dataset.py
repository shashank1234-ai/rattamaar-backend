import firebase_admin
from firebase_admin import credentials,firestore
import os
from PIL import Image,ImageFont,ImageDraw
import json
import math
import numpy as np

OUTPUT_DIR = os.getcwd()+'/Datasets/Images/s01/s01-000'
TEXT_DIR = os.getcwd()+'/Datasets'
print(OUTPUT_DIR)
cred = credentials.Certificate("ratta-maar-admin-34b55be5e70e.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
text_slicer = 89
def get_data(collection,template):
    # collection_data = db.collection(collection).stream()
    # print(collection_data)
    with open('pysics_question.json','r') as f:
        data = f.read()
        collection_data = json.loads(data)
        # print(collection_data)
    with open(TEXT_DIR+'/data_annotation.json') as fa:
        json_data = fa.read()
        annotates_json = json.loads(json_data)
    if(template == 'template1'):
        count=000
        for text in collection_data['phy_quest']:
            no_question_line = len(text['question'])/text_slicer
            question=''            
            for line in range(math.ceil(no_question_line)):
                question = question+ text['question'][line*text_slicer:(line+1)*text_slicer]+'\n'
            # print(question)
            # print(text['options'])
            # print(len(text['options']['A'])%text_slicer,text_slicer*0.75,text_slicer*0.5,text_slicer*0.25)
            # if len(text['options']['A'])/text_slicer>0 and len(text['options']['A'])/text_slicer<0.25:
            #     template = "template3"
            # elif len(text['options']['A'])/text_slicer>0.25 and len(text['options']['A'])/text_slicer<0.5:
            #     template = "template2"
            # elif len(text['options']['A'])/text_slicer>0.5:
            #     template = "template1"
            
            count=count+1
            img = Image.new("RGB", (3000, 1000), (0, 0, 0))
            title_font = ImageFont.truetype('gabriele-bad.ttf',50)
            image_editable = ImageDraw.Draw(img)
            # file_name = collection+'_'+template+'_'+str(count)
            file_name = "s01-000-s00-"+str(count)
            # if template == "template1":
            #     prepare_text = question+'\n\n'+'(A) '+text['options']['A']+'\n\n'+'(B) '+text['options']['B']+'\n\n'+'(C) '+text['options']['C']+'\n\n'+'(D) '+text['options']['D']
            #     # print(prepare_text)
            #     image_editable.text((100, 100),prepare_text,(255,255,255), font=title_font)
            #     img.save(file_name+".png", "PNG")
            # elif template == 'template2':
            #     prepare_text = question+'\n\n'+'(A) '+text['options']['A']+'    (B) '+text['options']['B']+'\n\n'+'(C) '+text['options']['C']+'     (D) '+text['options']['D']
            #     image_editable.text((100, 100),prepare_text,(255,255,255), font=title_font)
            #     img.save(file_name+".png", "PNG")
            # elif template == 'template3':
            #     prepare_text = question+'\n\n'+'(A) '+text['options']['A']+'    (B) '+text['options']['B']+'    (C) '+text['options']['C']+'    (D) '+text['options']['D']
            #     image_editable.text((100, 100),prepare_text,(255,255,255), font=title_font)
            #     img.save(file_name+".png", "PNG")
            # image_editable.text((100, 100),question,(255,255,255), font=title_font)
            # img.save(file_name+".png", "PNG")
            
            with open('sentences.txt','a') as fi:
                # print(annotates_json['_via_img_metadata'])
                img_data =json.dumps(annotates_json['_via_img_metadata'])
                for image_obj in json.loads(img_data):
                    print(annotates_json['_via_img_metadata'][image_obj])
                    print(annotates_json['_via_img_metadata'][image_obj]['regions'])
                    if file_name+'.png' == annotates_json['_via_img_metadata'][image_obj]['filename'] and len(annotates_json['_via_img_metadata'][image_obj]['regions'])!=0:
                        fi.writelines(file_name+'.png'+' 0 ok '+str(annotates_json['_via_img_metadata'][image_obj]['regions'][0]['shape_attributes']['x'])+' '+str(annotates_json['_via_img_metadata'][image_obj]['regions'][0]['shape_attributes']['y'])+' '+str(annotates_json['_via_img_metadata'][image_obj]['regions'][0]['shape_attributes']['width'])+' '+str(annotates_json['_via_img_metadata'][image_obj]['regions'][0]['shape_attributes']['width'])+' '+question.replace(' ','|'))

    
get_data('physics_questions','template1')
    
