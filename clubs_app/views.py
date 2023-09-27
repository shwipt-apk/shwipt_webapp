from flask import Flask
import firebase_admin
from firebase_admin import firestore
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

# Setting up the flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = '123456789qwert'

# Setting up the Firebase Database
firebase_app = firebase_admin.get_app()
firestore_db = firestore.client(app=firebase_app)
user_ref = firestore_db.collection('users')
club_ref = firestore_db.collection('clubs')
interest_ref = firestore_db.collection('interests')

@csrf_exempt
def get_user_club(request):
    if request.method == 'GET':
      try:
        data = json.loads(request.body)
        inputID = data.get('inputID')
        if not inputID:
          return JsonResponse({'message': 'inputID attribute is required'}, status=400)
        
        else:
          clubs = [doc.to_dict() for doc in club_ref.where("ownerID", "==", f"{inputID}").stream()]
          return JsonResponse({'status': 'Success', 'data': clubs, 'clubs_count': len(clubs)}, status=200)
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
        
@csrf_exempt
def get_joined_club(request):
    if request.method == 'GET':
      try:
        data = json.loads(request.body)
        inputID = data.get('inputID')
        if not inputID:
          return JsonResponse({'status': 'Failed', 'message': 'inputID attribute is required'}, status=400)
        
        else:
          req_doc = user_ref.document(f"{inputID}")
          joined_clubs_list = [doc.to_dict() for doc in req_doc.collection('joinedClubs').stream()]
          club_data_list = []

          for club_info in joined_clubs_list:
            club_id = club_info["clubID"]
            club_doc_ref = club_ref.document(club_id)
            club_data = club_doc_ref.get().to_dict()
    
            if club_data:
              club_data_list.append(club_data)
             
          return JsonResponse({'status': 'Success', 'data': club_data_list, 'clubs_count': len(joined_clubs_list)}, status=200)
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
        
@csrf_exempt
def get_explore_club(request):
    if request.method == 'GET':
      try:
        data = json.loads(request.body)
        inputID = data.get('inputID')
        if not inputID:
          return JsonResponse({'status': 'Failed', 'message': 'inputID attribute is required'}, status=400)
        
        else:
          club_list = [doc.to_dict()["clubID"] for doc in club_ref.stream()]
          req_doc = user_ref.document(f"{inputID}")
          
          if req_doc.collection('joinedClubs'):
            joined_clubs_list = [doc.to_dict()["clubID"] for doc in req_doc.collection('joinedClubs').get()]
          
          # To Get myClub uid list
          if req_doc.collection('myClubs'):
            myclubs_list = [doc.to_dict()["clubID"] for doc in req_doc.collection('myClubs').get()]

          for user_id in joined_clubs_list:
            try:
                club_list.remove(user_id)
            except ValueError:
                pass
    
          # To remove myClubs
          for user_id in myclubs_list:
            try:
                club_list.remove(user_id)
            except ValueError:
                pass
          
          joined_clubs_list = [doc.to_dict() for doc in req_doc.collection('joinedClubs').stream()]
          return JsonResponse({'status': 'Success', 'data': club_list, 'clubs_count': len(club_list)}, status=200)
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)

@csrf_exempt
def post_join_club(request):
    if request.method == 'POST':
      try:
        data = json.loads(request.body)
        inputID = data.get('inputID')
        clubID = data.get('clubID')
        ownerID = data.get('ownerID')

        if not inputID:
          return JsonResponse({'status': 'Failed', 'message': 'inputID attribute is required'}, status=400)
      
        
        if not clubID:
          return JsonResponse({'status': 'Failed', 'message': 'clubID attribute is required'}, status=400)
        
        if not ownerID:
          return JsonResponse({'status': 'Failed', 'message': 'ownerID attribute is required'}, status=400)
        
        else:
          newMemberCount = len([doc.to_dict() for doc in club_ref.document(clubID).collection('members').get()])
          updated_count = newMemberCount + 1

          post_club_data = {"uid": inputID, "role": "audience", "memberTime": firestore.SERVER_TIMESTAMP}
          post_user_data = {"clubID": clubID, "joinedTime": firestore.SERVER_TIMESTAMP}
          club_ref.document(clubID).update({'members': updated_count})
          club_ref.document(clubID).collection('members').document(inputID).set(post_club_data)
          user_ref.document(inputID).collection('joinedClubs').document(clubID).set(post_user_data)
          user_ref.document(ownerID).collection('myClubs').document(clubID).update({'members': updated_count})
          return JsonResponse({'status': 'Success', 'message': 'Joined Club Successfully'}, status=200)
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
        
@csrf_exempt
def post_create_club(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        inputID = data.get('inputID')
        clubName = data.get('clubName')
        description = data.get('description')
        imageUrl = data.get('imageUrl')
        isPrivate = data.get('isPrivate')
        interests = data.get('interests')

        if not inputID:
          return JsonResponse({'status': 'Failed', 'message': 'inputID attribute is required'}, status=400)
        
        if not clubName:
          return JsonResponse({'status': 'Failed', 'message': 'clubID attribute is required'}, status=400)
        
        if not description:
          return JsonResponse({'status': 'Failed', 'message': 'description attribute is required'}, status=400)
        
        else:
          new_ClubCount = len([doc.to_dict() for doc in club_ref.get()])
          club_ref.document('Club-'+str(new_ClubCount+1)).set({
             "clubID": 'Club-'+str(new_ClubCount+1),
             "clubName": clubName,
             "description": description,
             "createTime": firestore.SERVER_TIMESTAMP,
             "imageUrl": imageUrl,
             "members": 1,
             "ownerID": inputID,
             "private": isPrivate,
             "interests": interests
          })
          post_club_data = {"uid": inputID, "role": "owner", "memberTime": firestore.SERVER_TIMESTAMP}
          club_ref.document('Club-'+str(new_ClubCount+1)).collection('members').document(inputID).set(post_club_data)
          user_ref.document(inputID).collection('myClubs').document('Club-'+str(new_ClubCount+1)).set({
             "clubID": 'Club-'+str(new_ClubCount+1),
             "clubName": clubName,
             "description": description,
             "createTime": firestore.SERVER_TIMESTAMP,
             "imageUrl": imageUrl,
             "members": 1,
             "ownerID": inputID,
             "private": isPrivate,
             "interests": interests
          })
          return JsonResponse({'status': 'Success', 'message': 'Joined Club Successfully'}, status=200)
        
@csrf_exempt
def get_club_post(request):
    if request.method == 'GET':
      try:
        data = json.loads(request.body)
        clubID = data.get('clubID')
        if not clubID:
          return JsonResponse({'message': 'clubID attribute is required'}, status=400)
        
        else:
          clubs = [doc.to_dict() for doc in club_ref.document(clubID).collection('posts').order_by('postTime', direction=firestore.Query.DESCENDING).stream()]
          return JsonResponse({'status': 'Success', 'data': clubs, 'clubs_count': len(clubs)}, status=200)
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
    
    if request.method == 'POST':
      try:
        data = json.loads(request.body)
        clubID = data.get('clubID')
        inputID = data.get('inputID')
        username = data.get('username')
        displayPic = data.get('displayPic')
        clubName = data.get('clubName')
        clubPic = data.get('clubPic')
        description = data.get('description')
        imageUrl = data.get('imageUrl')
        interest = data.get('interest')

        if not clubID:
          return JsonResponse({'message': 'clubID attribute is required'}, status=400)
        
        else:
          new_feedCount = len([doc.to_dict() for doc in club_ref.document(clubID).collection('posts').get()])
          club_ref.document(clubID).collection('posts').document("Post-"+str(new_feedCount+1)).set({
            "description": description,
            "postTime": firestore.SERVER_TIMESTAMP,
            "uid": inputID,
            "username": username,
            "displayPic": displayPic,
            "likes": 0,
            "comments": 0,
            "imageUrl": imageUrl,
            "postID": "Post-"+str(new_feedCount+1),
            "deleted": False,
            "clubName": clubName,
            "clubPic": clubPic,
            "clubID": clubID,
            "interest": interest
          })

          return JsonResponse({'status': 'Success', 'message': 'Post Added Successfully!'}, status=200)
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)

@csrf_exempt
def get_club_updates(request):
    if request.method == 'GET':
      try:
        data = json.loads(request.body)
        clubID = data.get('clubID')
        if not clubID:
          return JsonResponse({'message': 'clubID attribute is required'}, status=400)
        
        else:
          clubs = [doc.to_dict() for doc in club_ref.document(clubID).collection('updates').order_by('postTime', direction=firestore.Query.DESCENDING).stream()]
          return JsonResponse({'status': 'Success', 'data': clubs, 'updates_count': len(clubs)}, status=200)
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
    
    if request.method == 'POST':
      try:
        data = json.loads(request.body)
        clubID = data.get('clubID')
        inputID = data.get('inputID')
        username = data.get('username')
        displayPic = data.get('displayPic')
        clubName = data.get('clubName')
        clubPic = data.get('clubPic')
        description = data.get('description')
        imageUrl = data.get('imageUrl')
        options = data.get('options')
        type = data.get('type')
        interests = data.get('interests')
        pollType = data.get('pollType')

        if not clubID:
          return JsonResponse({'message': 'clubID attribute is required'}, status=400)
        
        else:
          new_feedCount = len([doc.to_dict() for doc in club_ref.document(clubID).collection('updates').get()])
          updateID = "Updates-"+str(new_feedCount+1)

          club_ref.document(clubID).collection('updates').document("Updates-"+str(new_feedCount+1)).set({
              "description": description,
              "postTime": firestore.SERVER_TIMESTAMP,
              "uid": inputID,
              "username": username,
              "displayPic": displayPic,
              "likes": 0,
              "comments": 0,
              "imageUrl": imageUrl,
              "postID": "Update-"+str(new_feedCount+1),
              "deleted": False,
              "clubName": clubName,
              "clubPic": clubPic,
              "clubID": clubID,
              "options": options,
              "interests": interests,
              "type": type,
              "pollType": pollType,
          })

          return JsonResponse({'status': 'Success', 'message': 'Update Added Successfully!', 'updateID': updateID}, status=200)
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)

@csrf_exempt
def get_club_members(request):
    if request.method == 'GET':
      try:
        data = json.loads(request.body)
        clubID = data.get('clubID')
        if not clubID:
          return JsonResponse({'message': 'clubID attribute is required'}, status=400)
        
        else:
          members = [doc.to_dict() for doc in club_ref.document(clubID).collection('members').order_by('role', direction=firestore.Query.DESCENDING).stream()]
          member_data_list = []

          for club_info in members:
            memberID = club_info["uid"]
            member_doc_ref = user_ref.document(memberID)
            member_data = member_doc_ref.get().to_dict()
    
            if member_data:
              member_data_list.append(member_data)

          return JsonResponse({'status': 'Success', 'data': member_data_list, 'members_count': len(member_data_list)}, status=200)
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
      
@csrf_exempt
def get_club_interests(request):
    if request.method == 'GET':
      try:
        data = json.loads(request.body)
        inputID = data.get('inputID')
        if not inputID:
          return JsonResponse({'message': 'inputID attribute is required'}, status=400)
        
        else:
          interests = [doc.to_dict() for doc in interest_ref.order_by('interest', direction=firestore.Query.ASCENDING).stream()]
          return JsonResponse({'status': 'Success', 'data': interests, 'interests_count': len(interests)}, status=200)
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
      
    if request.method == 'POST':
      try:
        data = json.loads(request.body)
        interest = data.get('interest')
        if not interest:
          return JsonResponse({'message': 'interest attribute is required'}, status=400)
        
        else:
          interest_ref.document().set({
             "interest": interest
          })
          return JsonResponse({'status': 'Success', 'message': 'Interest Added!'}, status=200)
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
      
@csrf_exempt
def get_message_reacts(request):
    if request.method == 'GET':
      try:
        data = json.loads(request.body)
        messageID = data.get('messageID')
        clubID = data.get('clubID')

        if not messageID:
          return JsonResponse({'message': 'messageID attribute is required'}, status=400)
        
        if not clubID:
          return JsonResponse({'message': 'clubID attribute is required'}, status=400)
        
        else:
          reacts = [doc.to_dict() for doc in club_ref.document(clubID).collection('reactions').document(messageID).collection('message_reactions').order_by('reactTime', direction=firestore.Query.ASCENDING).stream()]
          return JsonResponse({'status': 'Success', 'data': reacts, 'interests_count': len(reacts)}, status=200)
        
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
      
    if request.method == 'POST':
      try:
        data = json.loads(request.body)
        messageID = data.get('messageID')
        clubID = data.get('clubID')
        reaction = data.get('reaction')
        username = data.get('username')
        displayPic = data.get('displayPic')
        inputID = data.get('inputID')

        if not messageID:
          return JsonResponse({'message': 'messageID attribute is required'}, status=400)
        
        if not clubID:
          return JsonResponse({'message': 'clubID attribute is required'}, status=400)
        
        if not reaction:
          return JsonResponse({'message': 'reaction attribute is required'}, status=400)
        
        if not username:
          return JsonResponse({'message': 'username attribute is required'}, status=400)
        
        if not displayPic:
          return JsonResponse({'message': 'displayPic attribute is required'}, status=400)
        
        if not inputID:
          return JsonResponse({'message': 'inputID attribute is required'}, status=400)
        
        else:
          club_ref.document(clubID).collection('reactions').document(messageID).collection('message_reactions').document().set({
             "inputID": inputID,
             "clubID": clubID,
             "reaction": reaction,
             "username": username,
             "displayPic": displayPic,
             "messageID": messageID,
             "reactTime": firestore.SERVER_TIMESTAMP
          })
          return JsonResponse({'status': 'Success', 'message': 'Reaction Added!'}, status=200)
        
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
      
@csrf_exempt
def get_react_exists(request):
    if request.method == 'GET':
      try:
        data = json.loads(request.body)
        messageID = data.get('messageID')
        clubID = data.get('clubID')
        inputID = data.get('inputID')

        if not messageID:
          return JsonResponse({'message': 'messageID attribute is required'}, status=400)
        
        if not clubID:
          return JsonResponse({'message': 'clubID attribute is required'}, status=400)
        
        if not inputID:
          return JsonResponse({'message': 'inputID attribute is required'}, status=400)
        
        else:
          reacts = [doc.to_dict() for doc in club_ref.document(clubID).collection('reactions').document(messageID).collection('message_reactions').where("inputID", "==", f"{inputID}").stream()]
          if len(reacts) > 0:
            return JsonResponse({'status': 'Success', 'message': 'React Exists', 'exists': True}, status=200)
          else:
            return JsonResponse({'status': 'Success', 'message': 'React Doesn\'t Exists', 'exists': False}, status=200)
        
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
      
@csrf_exempt
def get_post_likes(request):
    if request.method == 'GET':
      try:
        data = json.loads(request.body)
        postID = data.get('postID')
        clubID = data.get('clubID')

        if not postID:
          return JsonResponse({'message': 'postID attribute is required'}, status=400)
        
        if not clubID:
          return JsonResponse({'message': 'clubID attribute is required'}, status=400)
        
        else:
          query = club_ref.document(clubID).collection('posts').document(postID).collection('likes').order_by('postTime', direction=firestore.Query.DESCENDING)
          results = query.stream()
          all_likes = [{"id": likes.id, "data": likes.to_dict()} for likes in results]
          return JsonResponse({'message': 'Success', 'likes_data': all_likes, 'likes_count': len(all_likes)})
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
      
@csrf_exempt
def get_post_comments(request):
    if request.method == 'GET':
      try:
        data = json.loads(request.body)
        postID = data.get('postID')
        clubID = data.get('clubID')

        if not postID:
          return JsonResponse({'message': 'postID attribute is required'}, status=400)
        
        if not clubID:
          return JsonResponse({'message': 'clubID attribute is required'}, status=400)
        
        else:
          query = club_ref.document(clubID).collection('posts').document(postID).collection('comments').where("deleted", "==", False).order_by('postTime', direction=firestore.Query.DESCENDING)
          results = query.stream()
          all_comments = [{"id": comments.id, "data": comments.to_dict()} for comments in results]
          return JsonResponse({'message': 'Success', 'comments_data': all_comments, 'comments_count': len(all_comments)})
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
      
@csrf_exempt
def post_feed_likes(request):
    if request.method == 'POST':
      try:
        data = json.loads(request.body)
        postID = data.get('postID')
        clubID = data.get('clubID')
        uid = data.get('uid')
        displayPic = data.get('displayPic')
        username = data.get('username')

        if not postID:
          return JsonResponse({'message': 'postID attribute is required'}, status=400)
        
        elif not uid:
          return JsonResponse({'message': 'uid attribute is required'}, status=400)
        
        elif not displayPic:
          return JsonResponse({'message': 'displayPic attribute is required'}, status=400)
        
        elif not username:
          return JsonResponse({'message': 'username attribute is required'}, status=400)
        
        else:
          likersList = [doc.to_dict() for doc in club_ref.document(clubID).collection('posts').document(postID).collection('likes').where("uid", "==", f"{uid}").stream()]
          if len(likersList) == 0:
            get_like= club_ref.document(clubID).collection('posts').document(postID).get(field_paths={'likes'}).to_dict()
            current_count =  get_like.get('likes')
            updated_count = current_count + 1
            club_ref.document(clubID).collection('posts').document(postID).update({'likes': updated_count})
            club_ref.document(clubID).collection('posts').document(postID).collection('likes').document(uid).set({
              "postTime": firestore.SERVER_TIMESTAMP,
              "uid": uid,
              "username": username,
              "displayPic": displayPic,
            })
            return JsonResponse({'status': 'Success', 'message': 'Post Liked'})
          else:
            get_like= club_ref.document(clubID).collection('posts').document(postID).get(field_paths={'likes'}).to_dict()
            current_count =  get_like.get('likes')
            updated_count = current_count - 1
            club_ref.document(clubID).collection('posts').document(postID).update({'likes': updated_count})
            club_ref.document(clubID).collection('posts').document(postID).collection('likes').document(uid).delete()
            return JsonResponse({'status': 'Success', 'message': 'Post Unliked'})
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
      
@csrf_exempt
def post_feed_comments(request):
    if request.method == 'POST':
      try:
        data = json.loads(request.body)
        postID = data.get('postID')
        clubID = data.get('clubID')
        uid = data.get('uid')
        displayPic = data.get('displayPic')
        username = data.get('username')
        comment = data.get('comment')

        if not postID:
          return JsonResponse({'message': 'postID attribute is required'}, status=400)
        
        elif not uid:
          return JsonResponse({'message': 'uid attribute is required'}, status=400)
        
        elif not displayPic:
          return JsonResponse({'message': 'displayPic attribute is required'}, status=400)
        
        elif not username:
          return JsonResponse({'message': 'username attribute is required'}, status=400)
        
        elif not comment:
          return JsonResponse({'message': 'comment attribute is required'}, status=400)
        
        else:
          get_comment = club_ref.document(clubID).collection('posts').document(postID).get(field_paths={'comments'}).to_dict()
          current_count =  get_comment.get('comments')
          updated_count = current_count + 1
          club_ref.document(clubID).collection('posts').document(postID).update({'comments': updated_count})
          club_ref.document(clubID).collection('posts').document(postID).collection('comments').document("Comment-"+str(updated_count)).set({
            "postTime": firestore.SERVER_TIMESTAMP,
            "uid": uid,
            "username": username,
            "displayPic": displayPic,
            "comment": comment,
            "likes": 0,
            "deleted": False
          })
          return JsonResponse({'status': 'Success', 'message': 'Post Commented'})
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
    
    if request.method == 'PUT':
      try:
        data = json.loads(request.body)
        postID = data.get('postID')
        uid = data.get('uid')
        displayPic = data.get('displayPic')
        username = data.get('username')
        comment = data.get('comment')
        commentID = data.get('commentID')
        clubID = data.get('clubID')

        if not postID:
          return JsonResponse({'message': 'postID attribute is required'}, status=400)
        
        elif not uid:
          return JsonResponse({'message': 'uid attribute is required'}, status=400)
        
        elif not displayPic:
          return JsonResponse({'message': 'displayPic attribute is required'}, status=400)
        
        elif not username:
          return JsonResponse({'message': 'username attribute is required'}, status=400)
        
        elif not comment:
          return JsonResponse({'message': 'comment attribute is required'}, status=400)
        
        elif not commentID:
          return JsonResponse({'message': 'commentID attribute is required'}, status=400)
        
        else:
          get_comment = club_ref.document(clubID).collection('posts').document(postID).get(field_paths={'comments'}).to_dict()
          current_count =  get_comment.get('comments')
          updated_count = current_count - 1
          club_ref.document(clubID).collection('posts').document(postID).update({'comments': updated_count})
          # Updating Everything Because In Future We Might Be Showing (Someone Deleted Comment and People Can See If They Have Subscription)
          club_ref.document(clubID).collection('posts').document(postID).collection('comments').document(commentID).update({
            "postTime": firestore.SERVER_TIMESTAMP,
            "uid": uid,
            "username": username,
            "displayPic": displayPic,
            "comment": comment,
            "likes": 0,
            "deleted": True
          })
          return JsonResponse({'status': 'Success', 'message': 'Post Deleted'})
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
      
@csrf_exempt
def put_edit_club(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        inputID = data.get('inputID')
        clubID = data.get('clubID')
        clubName = data.get('clubName')
        description = data.get('description')
        imageUrl = data.get('imageUrl')

        if not inputID:
          return JsonResponse({'status': 'Failed', 'message': 'inputID attribute is required'}, status=400)

        if not clubID:
          return JsonResponse({'status': 'Failed', 'message': 'clubID attribute is required'}, status=400)
        
        if not clubName:
          return JsonResponse({'status': 'Failed', 'message': 'clubName attribute is required'}, status=400)
        
        if not description:
          return JsonResponse({'status': 'Failed', 'message': 'description attribute is required'}, status=400)
        
        if not imageUrl:
          return JsonResponse({'status': 'Failed', 'message': 'imageUrl attribute is required'}, status=400)
        
        else:
          
          club_ref.document(clubID).update({
             "clubName": clubName,
             "description": description,
             "imageUrl": imageUrl,
          })
          
          user_ref.document(inputID).collection('myClubs').document(clubID).update({
             "clubName": clubName,
             "description": description,
             "imageUrl": imageUrl
          })

          return JsonResponse({'status': 'Success', 'message': 'Edited Club Successfully'}, status=200)