from flask import Flask
import firebase_admin
from firebase_admin import firestore
from django.http import JsonResponse
import json
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt

# Setting up the flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = '123456789qwert'

# Setting up the Firebase Database
firebase_app = firebase_admin.get_app()
firestore_db = firestore.client(app=firebase_app)
user_ref = firestore_db.collection('users')
textStory_ref = firestore_db.collection('textStories')
photoStory_ref = firestore_db.collection('photoStories')
feeds_ref = firestore_db.collection('feeds')
club_ref = firestore_db.collection('clubs')
report_ref = firestore_db.collection('reports')

@csrf_exempt
def get_text_story(request):
    if request.method == 'GET':
      try:
        data = json.loads(request.body)
        inputID = data.get('inputID')
        query = textStory_ref.order_by('postTime', direction=firestore.Query.DESCENDING)
        results = query.stream()

        if not inputID:
          return JsonResponse({'message': 'inputID attribute is required'}, status=400)
        
        else:
          user_ids = [user.id for user in firestore_db.collection('users').document(inputID).collection('connections').stream()]
          all_text_stories = [{"id": stories.id, "data": stories.to_dict()} for stories in results if stories.id in user_ids or stories.id == inputID]
          return JsonResponse({'message': 'Success', 'story_data': all_text_stories, 'textStories_count': len(all_text_stories)})
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
    
    elif request.method == 'POST':
      try:
        data = json.loads(request.body)
        inputID = data.get('inputID')
        description = data.get('description')
        username = data.get('username')
        displayPic = data.get('displayPic')

        if not inputID:
          return JsonResponse({'message': 'inputID attribute is required'}, status=400)
        
        elif not description:
          return JsonResponse({'message': 'description attribute is required'}, status=400)
        
        elif not username:
          return JsonResponse({'message': 'username attribute is required'}, status=400)
        
        elif not displayPic:
          return JsonResponse({'message': 'displayPic attribute is required'}, status=400)
        
        else:
          textStory_ref.document(inputID).set({
            "description": description,
            "postTime": firestore.SERVER_TIMESTAMP,
            "uid": inputID,
            "username": username,
            "displayPic": displayPic,
            "likes": 0,
          })
          return JsonResponse({'status': 'Success', 'message': 'Text Story Created'})
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
      
@csrf_exempt
def get_photo_story(request):
    if request.method == 'GET':
      try:
        data = json.loads(request.body)
        inputID = data.get('inputID')

        if not inputID:
          return JsonResponse({'message': 'inputID attribute is required'}, status=400)
        
        else:
          final_list = []
          user_ids = [user.id for user in user_ref.document(inputID).collection('connections').stream()]
          user_ids.append(inputID)
          current_time = datetime.now()
          for user in user_ids:
            results = user_ref.document(user).collection('photoStories').stream()
            user_list = []
            for feed in results:
              feed_data = feed.to_dict()
              post_time = feed_data.get('postTime')
              time_difference = current_time - post_time
              if time_difference < timedelta(hours=24):
                user_list.append({"id": feed.id, "data": feed_data})
            if len(user_list) > 0:
              final_list.append({"userID": user, "user_story": user_list, "story_count": len(user_list)})
          return JsonResponse({'message': 'Success', 'story_data': final_list, 'photoStories_count': len(final_list)})
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
    
    elif request.method == 'POST':
      try:
        data = json.loads(request.body)
        inputID = data.get('inputID')
        description = data.get('description')
        username = data.get('username')
        displayPic = data.get('displayPic')
        imageUrl = data.get('imageUrl')

        if not inputID:
          return JsonResponse({'message': 'inputID attribute is required'}, status=400)
        
        elif not username:
          return JsonResponse({'message': 'username attribute is required'}, status=400)
        
        elif not displayPic:
          return JsonResponse({'message': 'displayPic attribute is required'}, status=400)
        
        elif not imageUrl:
          return JsonResponse({'message': 'imageUrl attribute is required'}, status=400)
        
        else:
          # photoStory_ref.document().set({
          #   "description": description,
          #   "postTime": firestore.SERVER_TIMESTAMP,
          #   "uid": inputID,
          #   "username": username,
          #   "displayPic": displayPic,
          #   "likes": 0,
          #   "imageUrl": imageUrl
          # })
          user_ref.document(inputID).collection('photoStories').document().set({
            "description": description,
            "postTime": firestore.SERVER_TIMESTAMP,
            "uid": inputID,
            "username": username,
            "displayPic": displayPic,
            "likes": 0,
            "imageUrl": imageUrl
          })
          return JsonResponse({'status': 'Success', 'message': 'Photo Story Created'})
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
      
@csrf_exempt
def get_worldwide_post(request):
    if request.method == 'GET':
      try:
        results = feeds_ref.order_by('postTime', direction=firestore.Query.DESCENDING).where("private", "==", False).stream()
        all_posts = [{"id": feed.id, "data": feed.to_dict()} for feed in results]
        return JsonResponse({'message': 'Success', 'feed_data': all_posts, 'feed_count': len(all_posts)})
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
    
    elif request.method == 'POST':
      try:
        data = json.loads(request.body)
        inputID = data.get('inputID')
        description = data.get('description')
        username = data.get('username')
        displayPic = data.get('displayPic')
        imageUrl = data.get('imageUrl')

        if not inputID:
          return JsonResponse({'message': 'inputID attribute is required'}, status=400)
        
        elif not username:
          return JsonResponse({'message': 'username attribute is required'}, status=400)
        
        elif not displayPic:
          return JsonResponse({'message': 'displayPic attribute is required'}, status=400)
        
        else:
          new_feedCount = len([doc.to_dict() for doc in feeds_ref.get()])
          feeds_ref.document("Post-"+str(new_feedCount+1)).set({
            "description": description,
            "postTime": firestore.SERVER_TIMESTAMP,
            "uid": inputID,
            "username": username,
            "displayPic": displayPic,
            "likes": 0,
            "comments": 0,
            "imageUrl": imageUrl,
            "private": False,
            "postID": "Post-"+str(new_feedCount+1),
            "deleted": False,
            "archived": False
          })
          return JsonResponse({'status': 'Success', 'message': 'Worldwide Post Created'}, status=200)
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
      
@csrf_exempt
def get_private_post(request):
    if request.method == 'GET':
      try:
        data = json.loads(request.body)
        inputID = data.get('inputID')
        results = feeds_ref.order_by('postTime', direction=firestore.Query.DESCENDING).where("private", "==", True).stream()

        if not inputID:
          return JsonResponse({'message': 'inputID attribute is required'}, status=400)
        
        else:
          user_ids = [user.id for user in firestore_db.collection('users').document(inputID).collection('connections').stream()]
          all_posts = [{"id": feed.id, "data": feed.to_dict()} for feed in results if feed.to_dict().get('uid') in user_ids]
          return JsonResponse({'message': 'Success', 'feed_data': all_posts, 'feed_count': len(all_posts)})
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
    
    elif request.method == 'POST':
      try:
        data = json.loads(request.body)
        inputID = data.get('inputID')
        description = data.get('description')
        username = data.get('username')
        displayPic = data.get('displayPic')
        displayName = data.get('displayName')
        imageUrl = data.get('imageUrl')

        if not inputID:
          return JsonResponse({'message': 'inputID attribute is required'}, status=400)
        
        elif not username:
          return JsonResponse({'message': 'username attribute is required'}, status=400)
        
        elif not displayPic:
          return JsonResponse({'message': 'displayPic attribute is required'}, status=400)
        
        else:
          new_feedCount = len([doc.to_dict() for doc in feeds_ref.get()])
          feeds_ref.document("Post-"+str(new_feedCount+1)).set({
            "description": description,
            "postTime": firestore.SERVER_TIMESTAMP,
            "uid": inputID,
            "username": username,
            "displayName": displayName,
            "displayPic": displayPic,
            "likes": 0,
            "comments": 0,
            "imageUrl": imageUrl,
            "private": True,
            "postID": "Post-"+str(new_feedCount+1),
            "deleted": False,
            "archived": False
          })
          return JsonResponse({'status': 'Success', 'message': 'Private Post Created'}, status=200)
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
      
@csrf_exempt
def get_post_likes(request):
    if request.method == 'GET':
      try:
        data = json.loads(request.body)
        postID = data.get('postID')
        query = feeds_ref.document(postID).collection('likes').order_by('postTime', direction=firestore.Query.DESCENDING)
        results = query.stream()

        if not postID:
          return JsonResponse({'message': 'postID attribute is required'}, status=400)
        
        else:
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
        query = feeds_ref.document(postID).collection('comments').where("deleted", "==", False).order_by('postTime', direction=firestore.Query.DESCENDING)
        results = query.stream()

        if not postID:
          return JsonResponse({'message': 'postID attribute is required'}, status=400)
        
        else:
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
          likersList = [doc.to_dict() for doc in feeds_ref.document(postID).collection('likes').where("uid", "==", f"{uid}").stream()]
          if len(likersList) == 0:
            get_like= feeds_ref.document(postID).get(field_paths={'likes'}).to_dict()
            current_count =  get_like.get('likes')
            updated_count = current_count + 1
            feeds_ref.document(postID).update({'likes': updated_count})
            feeds_ref.document(postID).collection('likes').document(uid).set({
              "postTime": firestore.SERVER_TIMESTAMP,
              "uid": uid,
              "username": username,
              "displayPic": displayPic,
            })
            return JsonResponse({'status': 'Success', 'message': 'Post Liked'})
          else:
            get_like= feeds_ref.document(postID).get(field_paths={'likes'}).to_dict()
            current_count =  get_like.get('likes')
            updated_count = current_count - 1
            feeds_ref.document(postID).update({'likes': updated_count})
            feeds_ref.document(postID).collection('likes').document(uid).delete()
            return JsonResponse({'status': 'Success', 'message': 'Post Unliked'})
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
      
@csrf_exempt
def post_feed_comments(request):
    if request.method == 'POST':
      try:
        data = json.loads(request.body)
        postID = data.get('postID')
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
          get_comment = feeds_ref.document(postID).get(field_paths={'comments'}).to_dict()
          current_count =  get_comment.get('comments')
          updated_count = current_count + 1
          feeds_ref.document(postID).update({'comments': updated_count})
          feeds_ref.document(postID).collection('comments').document("Comment-"+str(updated_count)).set({
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
          get_comment = feeds_ref.document(postID).get(field_paths={'comments'}).to_dict()
          current_count =  get_comment.get('comments')
          updated_count = current_count - 1
          feeds_ref.document(postID).update({'comments': updated_count})
          # Updating Everything Because In Future We Might Be Showing (Someone Deleted Comment and People Can See If They Have Subscription)
          feeds_ref.document(postID).collection('comments').document(commentID).update({
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
def get_user_club_post(request):
    if request.method == 'GET':
      try:
        data = json.loads(request.body)
        inputID = data.get('inputID')
      
        if not inputID:
          return JsonResponse({'message': 'inputID attribute is required'}, status=400)
    
        req_doc = user_ref.document(f"{inputID}")
        joined_clubs_list = []
        myclubs_list = []

        if req_doc.collection('joinedClubs'):
          joined_clubs_list = [doc.to_dict()["clubID"] for doc in req_doc.collection('joinedClubs').get()]

        if req_doc.collection('myClubs'):
          myclubs_list = [doc.to_dict()["clubID"] for doc in req_doc.collection('myClubs').get()]
    
        check_lst = set(joined_clubs_list + myclubs_list)
        print(check_lst)
        final_lst = []
        
        for _ in check_lst:
          new_doc = club_ref.document(f"{_}")
          post_lst = [doc.to_dict() for doc in new_doc.collection('posts').get()]
          for post in post_lst:
            final_lst.append({"id": post["postID"], "data": post})

        return JsonResponse({'status': 'Success', 'clubPost_data': final_lst, 'clubPost_count': len(final_lst)}, status=200)
      
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)

@csrf_exempt       
def post_feed_report(request):
    if request.method == 'POST':
      try:
        data = json.loads(request.body)
        inputID = data.get('inputID')
        postID = data.get('postID')
        reason = data.get('reason')
      
        if not inputID:
          return JsonResponse({'message': 'inputID attribute is required'}, status=400)
    
        elif not postID:
          return JsonResponse({'message': 'postID attribute is required'}, status=400)
        
        elif not reason:
          return JsonResponse({'message': 'reason attribute is required'}, status=400)
        
        else:
          feeds_ref.document(postID).collection('reports').document(inputID).set({
            "reportTime": firestore.SERVER_TIMESTAMP,
            "reportedBy": inputID,
            "reason": reason,
          })

          report_ref.document().set({
            "reportTime": firestore.SERVER_TIMESTAMP,
            "reportedBy": inputID,
            "reason": reason,
            "reportingTo": postID,
            "reportType": "feeds"
          })

          return JsonResponse({'status': 'Success', 'message': 'Post Reported!'}, status=200)
      
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
      
@csrf_exempt       
def put_delete_feed(request):
    if request.method == 'PUT':
      try:
        data = json.loads(request.body)
        postID = data.get('postID')
    
        if not postID:
          return JsonResponse({'message': 'postID attribute is required'}, status=400)
        
        else:
          feeds_ref.document(postID).update({
            "deleted": True
          })
          return JsonResponse({'status': 'Success', 'message': 'Post Deleted!'}, status=200)
      
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
      
@csrf_exempt       
def put_archive_feed(request):
    if request.method == 'GET':
      try:
        data = json.loads(request.body)
        inputID = data.get('inputID')
    
        if not inputID:
          return JsonResponse({'message': 'inputID attribute is required'}, status=400)
        
        else:
          archiveFeeds = [doc.to_dict() for doc in feeds_ref.where("uid", "==", f"{inputID}").where("archived", "==", True).where("deleted", "==", False).stream()]
          return JsonResponse({'status': 'Success', 'archiveData': archiveFeeds, 'archive_count': len(archiveFeeds)}, status=200)
      
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)

    if request.method == 'PUT':
      try:
        data = json.loads(request.body)
        postID = data.get('postID')
    
        if not postID:
          return JsonResponse({'message': 'postID attribute is required'}, status=400)
        
        else:
          feeds_ref.document(postID).update({
            "archived": True
          })
          return JsonResponse({'status': 'Success', 'message': 'Post Archived!'}, status=200)
      
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
      
@csrf_exempt       
def put_unarchive_feed(request):
    if request.method == 'PUT':
      try:
        data = json.loads(request.body)
        postID = data.get('postID')
    
        if not postID:
          return JsonResponse({'message': 'postID attribute is required'}, status=400)
        
        else:
          feeds_ref.document(postID).update({
            "archived": False
          })
          return JsonResponse({'status': 'Success', 'message': 'Post Un-Archived!'}, status=200)
      
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)

@csrf_exempt       
def put_like_comment(request):
    if request.method == 'POST':
      try:
        data = json.loads(request.body)
        postID = data.get('postID')
        commentID = data.get('commentID')
        inputID = data.get('inputID')
        username = data.get('username')
        displayPic = data.get('displayPic')
    
        if not postID:
          return JsonResponse({'message': 'postID attribute is required'}, status=400)
        
        elif not commentID:
          return JsonResponse({'message': 'commentID attribute is required'}, status=400)
        
        elif not inputID:
          return JsonResponse({'message': 'inputID attribute is required'}, status=400)
        
        else:
          likersList = [doc.to_dict() for doc in feeds_ref.document(postID).collection('comments').document(commentID).collection('likes').where("uid", "==", f"{inputID}").stream()]
          if len(likersList) == 0:
            get_like= feeds_ref.document(postID).collection('comments').document(commentID).get(field_paths={'likes'}).to_dict()
            current_count =  get_like.get('likes')
            updated_count = current_count + 1
            feeds_ref.document(postID).collection('comments').document(commentID).update({'likes': updated_count})
            feeds_ref.document(postID).collection('comments').document(commentID).collection('likes').document(inputID).set({
              "postTime": firestore.SERVER_TIMESTAMP,
              "uid": inputID,
              "username": username,
              "displayPic": displayPic,
            })
            return JsonResponse({'status': 'Success', 'message': 'Comment Liked!'}, status=200)
          else:
            get_like= feeds_ref.document(postID).collection('comments').document(commentID).get(field_paths={'likes'}).to_dict()
            current_count =  get_like.get('likes')
            updated_count = current_count - 1
            feeds_ref.document(postID).collection('comments').document(commentID).update({'likes': updated_count})
            feeds_ref.document(postID).collection('comments').document(commentID).collection('likes').document(inputID).delete()
            return JsonResponse({'status': 'Success', 'message': 'Comment Un-Liked!'}, status=200)
      
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)    

@csrf_exempt       
def post_story_view(request):
    if request.method == 'POST':
      try:
        data = json.loads(request.body)
        storyID = data.get('storyID')
        inputID = data.get('inputID')
        username = data.get('username')
        displayPic = data.get('displayPic')
    
        if not storyID:
          return JsonResponse({'message': 'storyID attribute is required'}, status=400)
        
        elif not inputID:
          return JsonResponse({'message': 'inputID attribute is required'}, status=400)
        
        else:
          photoStory_ref.document(storyID).collection('views').document(inputID).set({
            "postTime": firestore.SERVER_TIMESTAMP,
            "uid": inputID,
            "username": username,
            "displayPic": displayPic,
          })

          return JsonResponse({'message': 'Story Seen!', 'status': 'Success'}, status=200)
      
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
      
    if request.method == 'GET':
      try:
        data = json.loads(request.body)
        storyID = data.get('storyID')
        inputID = data.get('inputID')
    
        if not storyID:
          return JsonResponse({'message': 'storyID attribute is required'}, status=400)
        
        else:
          results = photoStory_ref.document(storyID).collection('views').order_by('postTime', direction=firestore.Query.DESCENDING).where("uid", "!=", inputID).stream()
          all_views = [{"id": views.id, "data": views.to_dict()} for views in results]
          return JsonResponse({'status': 'Success', 'views_data': all_views, 'views_count': len(all_views)})
      
      except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)