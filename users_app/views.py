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

firebase_app = firebase_admin.get_app()
firestore_db = firestore.client(app=firebase_app)

# Setting up theFirebase Database
user_ref = firestore_db.collection('users')
feeds_ref = firestore_db.collection('feeds')
report_ref = firestore_db.collection('reports')

@csrf_exempt
def get_user(request):
    if request.method == 'GET':
      try:
        data = json.loads(request.body)
        inputID = data.get('inputID')
        if not inputID:
          return JsonResponse({'message': 'inputID attribute is required'}, status=400)
        else:
          req_user = [doc.to_dict() for doc in user_ref.where("uid", "==", f"{inputID}").stream()]
          return JsonResponse({'message': 'Success', 'data': req_user})
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)

@csrf_exempt  
def get_alltime_popular(request):
    if request.method == 'GET':
      try:
        data = json.loads(request.body)
        inputID = data.get('inputID')
        gender = data.get('gender')
        country = data.get('country')
        query = user_ref.order_by('popularity', direction=firestore.Query.DESCENDING)
        results = query.stream()

        if not inputID:
          return JsonResponse({'message': 'inputID attribute is required'}, status=400)

        if not gender:
          return JsonResponse({'message': 'gender attribute is required'}, status=400)
        
        if not country:
          return JsonResponse({'message': 'country attribute is required'}, status=400)
        
        if gender == "Both":
          if country == "Worldwide":
            all_users = [{"id": user.id, "data": user.to_dict()} for user in results]
          else:
            all_users = [{"id": user.id, "data": user.to_dict()} for user in results if country == user.to_dict().get('country')]
        elif gender == "Male":
          if country == "Worldwide":
            all_users = [{"id": user.id, "data": user.to_dict()} for user in results if gender == user.to_dict().get('gender')]
          else:
            all_users = [{"id": user.id, "data": user.to_dict()} for user in results if country == user.to_dict().get('country') and gender == user.to_dict().get('gender')]
        else:
          if country == "Worldwide":
            all_users = [{"id": user.id, "data": user.to_dict()} for user in results if gender == user.to_dict().get('gender')]
          else:
            all_users = [{"id": user.id, "data": user.to_dict()} for user in results if  country == user.to_dict().get('country') and gender == user.to_dict().get('gender')]
        return JsonResponse({'message': 'Success', 'data': all_users, 'all_users': len(all_users)})
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)

@csrf_exempt
def get_weekly_popular(request):
    if request.method == 'GET':
      try:
        data = json.loads(request.body)
        inputID = data.get('inputID')
        gender = data.get('gender')
        country = data.get('country')
        query = user_ref.order_by('weekly_popularity', direction=firestore.Query.DESCENDING)
        results = query.stream()

        if not inputID:
          return JsonResponse({'message': 'inputID attribute is required'}, status=400)

        if not gender:
          return JsonResponse({'message': 'gender attribute is required'}, status=400)
        
        if not country:
          return JsonResponse({'message': 'country attribute is required'}, status=400)
        
        if gender == "Both":
          if country == "Worldwide":
            all_users = [{"id": user.id, "data": user.to_dict()} for user in results]
          else:
            all_users = [{"id": user.id, "data": user.to_dict()} for user in results if country == user.to_dict().get('country')]
        elif gender == "Male":
          if country == "Worldwide":
            all_users = [{"id": user.id, "data": user.to_dict()} for user in results if gender == user.to_dict().get('gender')]
          else:
            all_users = [{"id": user.id, "data": user.to_dict()} for user in results if country == user.to_dict().get('country') and gender == user.to_dict().get('gender')]
        else:
          if country == "Worldwide":
            all_users = [{"id": user.id, "data": user.to_dict()} for user in results if gender == user.to_dict().get('gender')]
          else:
            all_users = [{"id": user.id, "data": user.to_dict()} for user in results if  country == user.to_dict().get('country') and gender == user.to_dict().get('gender')]
        return JsonResponse({'message': 'Success', 'data': all_users, 'all_users': len(all_users)})
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)

@csrf_exempt
def get_active_user(request):
    if request.method == 'GET':
      try:
        data = json.loads(request.body)
        inputID = data.get('inputID')
        gender = data.get('gender')
        country = data.get('country')
        adminID = data.get('adminID')
        query = user_ref.order_by('last_active', direction=firestore.Query.DESCENDING)
        results = query.stream()

        if not inputID:
          return JsonResponse({'message': 'inputID attribute is required'}, status=400)

        if not gender:
          return JsonResponse({'message': 'gender attribute is required'}, status=400)
        
        if not country:
          return JsonResponse({'message': 'country attribute is required'}, status=400)
        
        if gender == "Both":
          if country == "Worldwide":
            all_users = [{"id": user.id, "data": user.to_dict()} for user in results if user.id != inputID and user.id != adminID and user.to_dict().get('active', True)]
          else:
            all_users = [{"id": user.id, "data": user.to_dict()} for user in results if user.id != inputID and user.id != adminID and country == user.to_dict().get('country') and user.to_dict().get('active', True)]
        elif gender == "Male":
          if country == "Worldwide":
            all_users = [{"id": user.id, "data": user.to_dict()} for user in results if user.id != inputID and user.id != adminID and gender == user.to_dict().get('gender') and user.to_dict().get('active', True)]
          else:
            all_users = [{"id": user.id, "data": user.to_dict()} for user in results if user.id != inputID and user.id != adminID and country == user.to_dict().get('country') and gender == user.to_dict().get('gender') and user.to_dict().get('active', True)]
        else:
          if country == "Worldwide":
            all_users = [{"id": user.id, "data": user.to_dict()} for user in results if user.id != inputID and user.id != adminID and gender == user.to_dict().get('gender') and user.to_dict().get('active', True)]
          else:
            all_users = [{"id": user.id, "data": user.to_dict()} for user in results if user.id != inputID and user.id != adminID and country == user.to_dict().get('country') and gender == user.to_dict().get('gender') and user.to_dict().get('active', True)]
        return JsonResponse({'message': 'Success', 'data': all_users, 'active_users': len(all_users)})
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)

@csrf_exempt
def get_active_friends(request):
    if request.method == 'GET':
      try:
        data = json.loads(request.body)
        inputID = data.get('inputID')
        gender = data.get('gender')
        country = data.get('country')
        adminID = data.get('adminID')

        if not inputID:
          return JsonResponse({'message': 'inputID attribute is required'}, status=400)
        
        if not gender:
          return JsonResponse({'message': 'gender attribute is required'}, status=400)
        
        if not country:
          return JsonResponse({'message': 'country attribute is required'}, status=400)
        
        req_doc = user_ref.document(f"{inputID}")
        active_connections = []
        if req_doc.collection('connections'):
          user_connections = [doc.to_dict() for doc in req_doc.collection('connections').get()]
          connection_uids = [connection['uid'] for connection in user_connections]

          if country == "Worldwide":
            if gender == "Both":
              active_users = (
                    user_ref
                    .where("uid", "in", connection_uids)
                    .where("active", "==", True)
                    .where("uid", "!=", adminID)
                    .get()
              )
            
            elif gender == "Male":
              active_users = (
                    user_ref
                    .where("uid", "in", connection_uids)
                    .where("active", "==", True)
                    .where("uid", "!=", adminID)
                    .where("gender", "==", "Male")
                    .get()
              )

            else:
              active_users = (
                    user_ref
                    .where("uid", "in", connection_uids)
                    .where("active", "==", True)
                    .where("uid", "!=", adminID)
                    .where("gender", "==", "Female")
                    .get()
              )
            
          else:
            if gender == "Both":
              active_users = (
                    user_ref
                    .where("uid", "in", connection_uids)
                    .where("active", "==", True)
                    .where("uid", "!=", adminID)
                    .get()
              )
            
            elif gender == "Male":
              active_users = (
                    user_ref
                    .where("uid", "in", connection_uids)
                    .where("active", "==", True)
                    .where("uid", "!=", adminID)
                    .where("gender", "==", "Male")
                    .get()
              )

            else:
              active_users = (
                    user_ref
                    .where("uid", "in", connection_uids)
                    .where("active", "==", True)
                    .where("uid", "!=", adminID)
                    .where("gender", "==", "Female")
                    .get()
              )

          active_connections = [
                    {"id": doc.id, "data": doc.to_dict()}
                    for doc in active_users
          ]
        
        else:
          return JsonResponse({'message': 'Failed', 'data': active_connections})
        
        return JsonResponse({'message': 'Success', 'data': active_connections, 'active_users': len(active_connections)})
      
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
      
@csrf_exempt
def post_create_user(request):
    if request.method == 'POST':
      try:
        data = json.loads(request.body)
        uid = data.get('uid')
        data['lastActive'] = firestore.SERVER_TIMESTAMP

        user_ref.document(uid).set(data)
        return JsonResponse({'status': 'Success', 'message': 'User Created Successfully'})
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
      
@csrf_exempt
def get_user_existence(request):
    if request.method == 'GET':
      try:
        data = json.loads(request.body)
        email = data.get('email')
        req_user = [doc.to_dict() for doc in user_ref.where("email", "==", f"{email}").stream()]
        if len(req_user) > 0:
          return JsonResponse({'status': 'Success', 'message': 'E-Mail Exists', 'exists': True})
        else:
          return JsonResponse({'status': 'Success', 'message': 'E-Mail Doesn\'t Exists', 'exists': False})
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
      
@csrf_exempt
def get_email_existence(request):
    if request.method == 'GET':
      try:
        data = json.loads(request.body)
        phone = data.get('email')
        req_user = [doc.to_dict() for doc in user_ref.where("phone", "==", f"{phone}").stream()]
        if len(req_user) > 0:
          return JsonResponse({'status': 'Success', 'message': 'User Exists', 'exists': True})
        else:
          return JsonResponse({'status': 'Success', 'message': 'User Doesn\'t Exists', 'exists': False})
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
      
@csrf_exempt
def put_edit_userProfile(request):
    if request.method == 'PUT':
      try:
        data = json.loads(request.body)
        inputID = data.get('inputID')

        if not inputID:
          return JsonResponse({'message': 'inputID attribute is required'}, status=400)
        
        else:
          user_ref.document(inputID).update(data)
          return JsonResponse({'status': 'Success', 'message': 'Profile Updated'})
        
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
      
@csrf_exempt
def get_user_post(request):
    if request.method == 'GET':
      try:
        data = json.loads(request.body)
        inputID = data.get('inputID')

        if not inputID:
          return JsonResponse({'message': 'inputID attribute is required'}, status=400)
        
        else:
          results = feeds_ref.order_by('postTime', direction=firestore.Query.DESCENDING).where("uid", "==", inputID).stream()
          all_posts = [{"id": feed.id, "data": feed.to_dict()} for feed in results]
          return JsonResponse({'status': 'Success', 'feed_data': all_posts, 'feed_count': len(all_posts)})
        
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
      
@csrf_exempt
def post_user_request(request):
    if request.method == 'POST':
      try:
        data = json.loads(request.body)
        senderID = data.get('senderID')
        displayName = data.get('displayName')
        displayPic = data.get('displayPic')
        age = data.get('age')
        gender = data.get('gender')
        flag = data.get('flag')
        country = data.get('country')
        receiverID = data.get('receiverID')

        if not senderID:
          return JsonResponse({'message': 'senderID attribute is required'}, status=400)
        
        elif not displayName:
          return JsonResponse({'message': 'displayName attribute is required'}, status=400)
        
        elif not displayPic:
          return JsonResponse({'message': 'displayPic attribute is required'}, status=400)
        
        elif not age:
          return JsonResponse({'message': 'age attribute is required'}, status=400)
        
        elif not gender:
          return JsonResponse({'message': 'gender attribute is required'}, status=400)
        
        elif not flag:
          return JsonResponse({'message': 'flag attribute is required'}, status=400)
        
        elif not country:
          return JsonResponse({'message': 'country attribute is required'}, status=400)
        
        elif not receiverID:
          return JsonResponse({'message': 'receiverID attribute is required'}, status=400)
        
        else:
          user_ref.document(receiverID).collection('requests').doc(senderID).set(data)
          user_ref.document(senderID).collection('sentRequests').doc(receiverID).set({
            "receiverID": receiverID
          })
          return JsonResponse({'status': 'Success', 'message': 'Request Sent!'})
        
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
      
@csrf_exempt
def post_request_accept(request):
    if request.method == 'POST':
      try:
        data = json.loads(request.body)
        senderID = data.get('senderID')
        senderDisplayName = data.get('senderDisplayName')
        senderDisplayPic = data.get('senderDisplayPic')
        senderAge = data.get('senderAge')
        senderGender = data.get('senderGender')
        senderFlag = data.get('senderFlag')
        senderCountry = data.get('senderCountry')
        receiverID = data.get('receiverID')
        receiverDisplayName = data.get('receiverDisplayName')
        receiverDisplayPic = data.get('receiverDisplayPic')
        receiverAge = data.get('receiverAge')
        receiverGender = data.get('receiverGender')
        receiverFlag = data.get('receiverFlag')
        receiverCountry = data.get('receiverCountry')

        if not senderID:
          return JsonResponse({'message': 'senderID attribute is required'}, status=400)
        
        elif not senderDisplayName:
          return JsonResponse({'message': 'senderDisplayName attribute is required'}, status=400)
        
        elif not senderDisplayPic:
          return JsonResponse({'message': 'senderDisplayPic attribute is required'}, status=400)
        
        elif not senderAge:
          return JsonResponse({'message': 'senderAge attribute is required'}, status=400)
        
        elif not senderGender:
          return JsonResponse({'message': 'senderGender attribute is required'}, status=400)
        
        elif not senderFlag:
          return JsonResponse({'message': 'senderFlag attribute is required'}, status=400)
        
        elif not senderCountry:
          return JsonResponse({'message': 'senderCountry attribute is required'}, status=400)
        
        elif not receiverID:
          return JsonResponse({'message': 'receiverID attribute is required'}, status=400)
        
        elif not receiverDisplayName:
          return JsonResponse({'message': 'receiverDisplayName attribute is required'}, status=400)
        
        elif not receiverDisplayPic:
          return JsonResponse({'message': 'receiverDisplayPic attribute is required'}, status=400)
        
        elif not receiverAge:
          return JsonResponse({'message': 'receiverAge attribute is required'}, status=400)
        
        elif not receiverGender:
          return JsonResponse({'message': 'receiverGender attribute is required'}, status=400)
        
        elif not receiverFlag:
          return JsonResponse({'message': 'receiverFlag attribute is required'}, status=400)
        
        elif not receiverCountry:
          return JsonResponse({'message': 'receiverCountry attribute is required'}, status=400)
        
        else:
          user_ref.document(receiverID).collection('requests').doc(senderID).set({
            "uid": senderID,
            "flag": senderFlag,
            "gender": senderGender,
            "displayName": senderDisplayName,
            "displayPic": senderDisplayPic,
            "age": senderAge,
            "country": senderCountry
          })

          user_ref.document(senderID).collection('sentRequests').doc(receiverID).set({
            "uid": receiverID,
            "flag": receiverFlag,
            "gender": receiverGender,
            "displayName": receiverDisplayName,
            "displayPic": receiverDisplayPic,
            "age": receiverAge,
            "country": receiverCountry
          })

          user_ref.document(receiverID).collection('requests').doc(senderID).delete()
          user_ref.document(senderID).collection('sentRequests').doc(receiverID).delete()

          return JsonResponse({'status': 'Success', 'message': 'Request Accepted!'})
        
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
      
@csrf_exempt
def post_request_reject(request):
    if request.method == 'POST':
      try:
        data = json.loads(request.body)
        senderID = data.get('senderID')
        receiverID = data.get('receiverID')

        if not senderID:
          return JsonResponse({'message': 'senderID attribute is required'}, status=400)
        
        elif not receiverID:
          return JsonResponse({'message': 'receiverID attribute is required'}, status=400)
        
        else:
          user_ref.document(receiverID).collection('requests').doc(senderID).delete()
          user_ref.document(senderID).collection('sentRequests').doc(receiverID).delete()

          return JsonResponse({'status': 'Success', 'message': 'Request Rejected!'})
        
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
      
@csrf_exempt
def put_cancel_request(request):
    if request.method == 'PUT':
      try:
        data = json.loads(request.body)
        senderID = data.get('senderID')
        receiverID = data.get('receiverID')

        if not senderID:
          return JsonResponse({'message': 'senderID attribute is required'}, status=400)
        
        elif not receiverID:
          return JsonResponse({'message': 'receiverID attribute is required'}, status=400)
        
        else:
          user_ref.document(receiverID).collection('requests').doc(senderID).delete()
          user_ref.document(senderID).collection('sentRequests').doc(receiverID).delete()
          return JsonResponse({'status': 'Success', 'message': 'Request Canceled!'})
        
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)

@csrf_exempt
def put_user_unfriend(request):
    if request.method == 'PUT':
      try:
        data = json.loads(request.body)
        senderID = data.get('senderID')
        receiverID = data.get('receiverID')

        if not senderID:
          return JsonResponse({'message': 'senderID attribute is required'}, status=400)
        
        elif not receiverID:
          return JsonResponse({'message': 'receiverID attribute is required'}, status=400)
        
        else:
          user_ref.document(receiverID).collection('connections').doc(senderID).delete()
          user_ref.document(senderID).collection('connections').doc(receiverID).delete()

          return JsonResponse({'status': 'Success', 'message': 'Request Rejected!'})
        
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)

@csrf_exempt
def get_user_connection(request):
    if request.method == 'GET':
      try:
        data = json.loads(request.body)
        senderID = data.get('senderID')
        receiverID = data.get('receiverID')

        if not senderID:
          return JsonResponse({'message': 'senderID attribute is required'}, status=400)
        
        if not receiverID:
          return JsonResponse({'message': 'receiverID attribute is required'}, status=400)
        
        else:
          req_user = [doc.to_dict() for doc in user_ref.document(receiverID).collection('requests').where("senderID", "==", f"{senderID}").stream()]
          con_user = [doc.to_dict() for doc in user_ref.document(receiverID).collection('connections').where("uid", "==", f"{senderID}").stream()]
          blocked_user = [doc.to_dict() for doc in user_ref.document(receiverID).collection('blocks').where("blockedBy", "==", f"{senderID}").stream()]
          blocked_user2 = [doc.to_dict() for doc in user_ref.document(senderID).collection('blocks').where("blockedBy", "==", f"{receiverID}").stream()]
          reported_user = [doc.to_dict() for doc in user_ref.document(receiverID).collection('reports').where("reportedBy", "==", f"{senderID}").stream()]
          reported_user2 = [doc.to_dict() for doc in user_ref.document(senderID).collection('reports').where("reportedBy", "==", f"{receiverID}").stream()]
          
          if len(req_user) != 0:
            return JsonResponse({'status': 'Success', 'message': 'Requested'})
          
          elif len(con_user) != 0:
            return JsonResponse({'status': 'Success', 'message': 'Connected'})
          
          elif len(blocked_user) != 0 or len(blocked_user2) != 0:
            return JsonResponse({'status': 'Success', 'message': 'Blocked'})
          
          elif len(reported_user) != 0 or len(reported_user2) != 0:
            return JsonResponse({'status': 'Success', 'message': 'Reported'})
          
          else:
            return JsonResponse({'status': 'Success', 'message': 'Stranger', 'len': len(con_user)})
        
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
      
@csrf_exempt
def put_edit_userSocial(request):
    if request.method == 'PUT':
      try:
        data = json.loads(request.body)
        inputID = data.get('inputID')

        if not inputID:
          return JsonResponse({'message': 'inputID attribute is required'}, status=400)
        
        else:
          user_ref.document(inputID).update(data)
          return JsonResponse({'status': 'Success', 'message': 'User Social Updated'})
        
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
      
@csrf_exempt       
def post_user_report(request):
    if request.method == 'POST':
      try:
        data = json.loads(request.body)
        inputID = data.get('inputID')
        reportingID = data.get('reportingID')
        reason = data.get('reason')
      
        if not inputID:
          return JsonResponse({'message': 'inputID attribute is required'}, status=400)
    
        elif not reportingID:
          return JsonResponse({'message': 'reportingID attribute is required'}, status=400)
        
        elif not reason:
          return JsonResponse({'message': 'reason attribute is required'}, status=400)
        
        else:

          req_user = [doc.to_dict() for doc in user_ref.document(reportingID).collection('requests').where("senderID", "==", f"{inputID}").stream()]
          req_user2 = [doc.to_dict() for doc in user_ref.document(inputID).collection('requests').where("senderID", "==", f"{reportingID}").stream()]
          con_user = [doc.to_dict() for doc in user_ref.document(reportingID).collection('connections').where("uid", "==", f"{inputID}").stream()]          
          blocked_user = [doc.to_dict() for doc in user_ref.document(reportingID).collection('blocks').where("blockedBy", "==", f"{inputID}").stream()]
          blocked_user2 = [doc.to_dict() for doc in user_ref.document(inputID).collection('blocks').where("blockedBy", "==", f"{reportingID}").stream()]
          
          user_ref.document(reportingID).collection('reports').document(inputID).set({
            "reportTime": firestore.SERVER_TIMESTAMP,
            "reportedBy": inputID,
            "reason": reason,
          })

          user_ref.document(inputID).collection('reported').document(reportingID).set({
            "reportTime": firestore.SERVER_TIMESTAMP,
            "reported": reportingID,
            "reason": reason,
          })

          report_ref.document().set({
            "reportTime": firestore.SERVER_TIMESTAMP,
            "reportedBy": inputID,
            "reason": reason,
            "reportingTo": reportingID,
            "reportType": "user"
          })

          if len(req_user) != 0:
            user_ref.document(reportingID).collection('requests').document(inputID).delete()
            user_ref.document(inputID).collection('requested').document(reportingID).delete()
            
          elif len(req_user2) != 0:
            user_ref.document(inputID).collection('requests').document(reportingID).delete()
            user_ref.document(reportingID).collection('requested').document(inputID).delete()
            
          elif len(con_user) != 0:
            user_ref.document(reportingID).collection('connections').document(inputID).delete()
            user_ref.document(inputID).collection('connections').document(reportingID).delete()
          
          elif len(blocked_user) != 0:
            user_ref.document(reportingID).collection('blocks').document(inputID).delete()
            user_ref.document(inputID).collection('blocked').document(reportingID).delete()
          
          elif len(blocked_user2) != 0:
            user_ref.document(inputID).collection('blocks').document(reportingID).delete()
            user_ref.document(reportingID).collection('blocked').document(inputID).delete()
            
          return JsonResponse({'status': 'Success', 'message': 'User Reported!'}, status=200)
      
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
      
@csrf_exempt       
def post_user_block(request):
    if request.method == 'POST':
      try:
        data = json.loads(request.body)
        inputID = data.get('inputID')
        blockingID = data.get('blockingID')
      
        if not inputID:
          return JsonResponse({'message': 'inputID attribute is required'}, status=400)
    
        elif not blockingID:
          return JsonResponse({'message': 'reportingID attribute is required'}, status=400)
        
        else:
          req_user = [doc.to_dict() for doc in user_ref.document(blockingID).collection('requests').where("senderID", "==", f"{inputID}").stream()]
          req_user2 = [doc.to_dict() for doc in user_ref.document(inputID).collection('requests').where("senderID", "==", f"{blockingID}").stream()]
          con_user = [doc.to_dict() for doc in user_ref.document(blockingID).collection('connections').where("uid", "==", f"{inputID}").stream()]          
          report_user = [doc.to_dict() for doc in user_ref.document(blockingID).collection('reports').where("reportedBy", "==", f"{inputID}").stream()]
          report_user2 = [doc.to_dict() for doc in user_ref.document(inputID).collection('reports').where("reportedBy", "==", f"{blockingID}").stream()]

          user_ref.document(blockingID).collection('blocks').document(inputID).set({
            "blockTime": firestore.SERVER_TIMESTAMP,
            "blockedBy": inputID,
          })

          user_ref.document(inputID).collection('blocked').document(blockingID).set({
            "blockTime": firestore.SERVER_TIMESTAMP,
            "blocked": blockingID,
          })

          if len(req_user) != 0:
            user_ref.document(blockingID).collection('requests').document(inputID).delete()
            user_ref.document(inputID).collection('requested').document(blockingID).delete()
            
          elif len(req_user2) != 0:
            user_ref.document(inputID).collection('requests').document(blockingID).delete()
            user_ref.document(blockingID).collection('requested').document(inputID).delete()
            
          elif len(con_user) != 0:
            user_ref.document(blockingID).collection('connections').document(inputID).delete()
            user_ref.document(inputID).collection('connections').document(blockingID).delete()
          
          elif len(report_user) != 0:
            user_ref.document(blockingID).collection('reports').document(inputID).delete()
            user_ref.document(inputID).collection('reported').document(blockingID).delete()
          
          elif len(report_user2) != 0:
            user_ref.document(inputID).collection('reports').document(blockingID).delete()
            user_ref.document(blockingID).collection('reported').document(inputID).delete()

          return JsonResponse({'status': 'Success', 'message': 'User Blocked!'}, status=200)
      
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
      
@csrf_exempt
def get_friends(request):
    if request.method == 'GET':
      try:
        data = json.loads(request.body)
        inputID = data.get('inputID')
        gender = data.get('gender')
        country = data.get('country')

        if not inputID:
          return JsonResponse({'message': 'inputID attribute is required'}, status=400)
        
        if not gender:
          return JsonResponse({'message': 'gender attribute is required'}, status=400)
        
        if not country:
          return JsonResponse({'message': 'country attribute is required'}, status=400)
        
        req_doc = user_ref.document(f"{inputID}")
        active_connections = []
        if req_doc.collection('connections'):
          user_connections = [doc.to_dict() for doc in req_doc.collection('connections').get()]
          connection_uids = [connection['uid'] for connection in user_connections]

          if country == "Worldwide":
            if gender == "Both":
              active_users = (
                    user_ref
                    .where("uid", "in", connection_uids)
                    .get()
              )
            
            elif gender == "Male":
              active_users = (
                    user_ref
                    .where("uid", "in", connection_uids)
                    .where("gender", "==", "Male")
                    .get()
              )

            else:
              active_users = (
                    user_ref
                    .where("uid", "in", connection_uids)
                    .where("gender", "==", "Female")
                    .get()
              )
            
          else:
            if gender == "Both":
              active_users = (
                    user_ref
                    .where("uid", "in", connection_uids)
                    .get()
              )
            
            elif gender == "Male":
              active_users = (
                    user_ref
                    .where("uid", "in", connection_uids)
                    .where("gender", "==", "Male")
                    .get()
              )

            else:
              active_users = (
                    user_ref
                    .where("uid", "in", connection_uids)
                    .where("gender", "==", "Female")
                    .get()
              )

          active_connections = [
                    {"id": doc.id, "data": doc.to_dict()}
                    for doc in active_users
          ]
        
        else:
          return JsonResponse({'message': 'Failed', 'data': active_connections})
        
        return JsonResponse({'message': 'Success', 'data': active_connections, 'friends_count': len(active_connections)})
      
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)