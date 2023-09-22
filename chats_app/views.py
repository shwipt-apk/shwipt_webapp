from flask import Flask
import firebase_admin
from firebase_admin import firestore
from django.http import JsonResponse
import json
import datetime
from django.views.decorators.csrf import csrf_exempt

# Setting up the flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = '123456789qwert'

# Setting up the Firebase Database
firebase_app = firebase_admin.get_app()
firestore_db = firestore.client(app=firebase_app)
admin_ref = firestore_db.collection('admin')
user_ref = firestore_db.collection('users')

@csrf_exempt
def get_chat_history(request):
    if request.method == 'GET':
      try:
        data = json.loads(request.body)
        inputID = data.get('inputID')
        if not inputID:
          return JsonResponse({'message': 'inputID attribute is required'}, status=400)
        else:
            chat_data = [doc.to_dict() for doc in user_ref.document(input).collection('chatHistory').stream()]
            return JsonResponse({'message': 'Success', 'chat_data': chat_data})
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
    
    if request.method == 'POST':
       try:
          data = json.loads(request.body)
          senderID = data.get('inputID')
          receiverID = data.get('receiverID')
          message = data.get('message')
          senderUsername = data.get('senderUsername')
          senderDisplayPic = data.get('senderDisplayPic')
          senderflag = data.get('senderflag')
          receiverUsername = data.get('receiverUsername')
          receiverDisplayPic = data.get('receiverDisplayPic')
          receiverflag = data.get('receiverflag')

          if not senderID:
           return JsonResponse({'message': 'senderID attribute is required'}, status=400)
          
          if not receiverID:
           return JsonResponse({'message': 'receiverID attribute is required'}, status=400)
          
          if not message:
           return JsonResponse({'message': 'message attribute is required'}, status=400)
          
          if not senderUsername:
           return JsonResponse({'message': 'senderUsername attribute is required'}, status=400)
          
          if not senderDisplayPic:
           return JsonResponse({'message': 'senderDisplayPic attribute is required'}, status=400)
          
          if not senderflag:
           return JsonResponse({'message': 'senderflag attribute is required'}, status=400)
          
          if not receiverUsername:
           return JsonResponse({'message': 'receiverUsername attribute is required'}, status=400)
          
          if not receiverDisplayPic:
           return JsonResponse({'message': 'receiverDisplayPic attribute is required'}, status=400)
          
          if not receiverflag:
           return JsonResponse({'message': 'receiverflag attribute is required'}, status=400)
          
          result = senderID + "_" + receiverID if senderID < receiverID else receiverID + "_" + senderID
          user_ref.document(senderID).collection('chatHistory').document(result).set({
            "senderID": senderID,
            "receiverID": receiverID,
            "message": message,
            "username": receiverUsername,
            "displayPic": receiverDisplayPic,
            "flag": receiverflag
          })
          
          user_ref.document(receiverID).collection('chatHistory').document(result).set({
            "senderID": senderID,
            "receiverID": receiverID,
            "message": message,
            "username": senderUsername,
            "displayPic": senderDisplayPic,
            "flag": senderflag
          })
          return JsonResponse({'message': 'Added Successfully!'}, status=400)
          
       except Exception as e:
          return JsonResponse({'message': str(e)}, status=500)