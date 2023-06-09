from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied

import jwt
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.conf import settings

from .serializers.common import UserSerializer, UserCollection, UserWishlist, UserFollowing, UserInfo
from .serializers.populated import PopulatedUserSerializer

from records.models import Record
from records.serializers.common import RecordSerializer

from lib.exceptions import exceptions

User = get_user_model()

# Create your views here.
class RegisterView(APIView):
    
    #Register Route
    #Endpoint: /api/auth/register/

    @exceptions
    def post(self, request):
        print('REQUEST DATA =>', request.data)
        new_user = UserSerializer(data=request.data)
        new_user.is_valid(raise_exception=True)
        new_user.save()
        return Response(new_user.data, status.HTTP_201_CREATED)
    
class LoginView(APIView):
    
    #Login Route
    #Endpoint: /api/auth/login/
    @exceptions
    def post(self, request):
        print('LOGIN ROUTE HIT')
        email = request.data['email']
        password = request.data['password']
        user_to_login = User.objects.get(email=email)

        if not user_to_login.check_password(password):
          print('PASSWORDS DO NOT MATCH')
          raise PermissionDenied('Unauthorized')
        
        print('USER TO LOGIN ID', user_to_login.id)
        dt = datetime.now() + timedelta(days=2)
        exp = int(dt.strftime('%s'))
        print(exp)
        
        token = jwt.encode({ 'sub': user_to_login.id, 'exp': exp }, settings.SECRET_KEY, algorithm='HS256')
        print('TOKEN', token)
        
        return Response({ 'message': f'Welcome back, {user_to_login}', 'token': token })
    
class ProfileView(APIView):
    
    @exceptions
    def get(self, request, id):
        print('PROFILE ROUTE HIT')
        print('USER ID =>', id)
        user = User.objects.get(id=id)
        serialized_user = PopulatedUserSerializer(user)
        return Response(serialized_user.data)
    
    @exceptions
    def put(self, request, id):
        user = User.objects.get(id=id)
        serialized_user = UserInfo(user, request.data, partial=True)
        serialized_user.is_valid(raise_exception=True)
        serialized_user.save()
        return Response(serialized_user.data)
    
    @exceptions
    def delete(self, request, id):
        user = User.objects.get(id=id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
class AllProfiles(APIView):
    
    @exceptions
    def get(self, request):
        print('PROFILE ROUTE HIT')
        user = User.objects.all()
        serialized_user = UserInfo(user, many=True)
        return Response(serialized_user.data)    
    
class AddRecordToCollectionView(APIView):
    
    @exceptions
    def put(self, request, id1, id2):
        
        #Retrieve both the user profile and the record
        user = User.objects.get(id=id1)
        record = Record.objects.get(id=id2)
        
        #Serialize record instance and save to variable
        serialized_record = RecordSerializer(record)

        #Save record data to variable
        to_add = serialized_record.data

        #Serialize User instance and save to variable
        serialized_user = UserCollection(user)

        #Save User data to variable
        to_update = serialized_user.data

        #Append the Record ID to the User Collection
        to_update['collection'].append(to_add['id'])

        #Update/Validate/Save and return User with updated collection field
        final = UserCollection(user, to_update, partial=True)

        final.is_valid(raise_exception=True)
        final.save()

        wishlist = UserWishlist(user)

        wl_update = wishlist.data

        print('WISHLIST =>', wl_update)

        if to_add['id'] in wl_update['wishlist']:
            wl_update['wishlist'].remove(to_add['id'])
            fin_wl_update = UserWishlist(user, wl_update, partial=True)
            fin_wl_update.is_valid(raise_exception=True)
            fin_wl_update.save()

        return Response(final.data)

class AddRecordToWishlistView(APIView):
    
    @exceptions
    def put(self, request, id1, id2):
        
        #Retrieve both the user profile and the record
        user = User.objects.get(id=id1)
        record = Record.objects.get(id=id2)
        
        #Serialize record instance and save to variable
        serialized_record = RecordSerializer(record)

        #Save record data to variable
        to_add = serialized_record.data

        #Serialize User instance and save to variable
        serialized_user = UserWishlist(user)

        collection = UserCollection(user)
        to_check = collection.data

        #Save User data to variable
        to_update = serialized_user.data


        #Check to see if record to be added to wishlist is not already in collection
        if not to_add['id'] in to_check['collection']:
            #Append the Record ID to the User Collection
            to_update['wishlist'].append(to_add['id'])

            #Update/Validate/Save and return User with updated collection field
            final = UserWishlist(user, to_update, partial=True)

            final.is_valid(raise_exception=True)
            final.save()
            return Response(final.data)
        
        else:
            return Response({ 'message': 'Record is already in your collection.' })

class RemoveRecordFromCollection(APIView):
    
    @exceptions
    def put(self, request, id1, id2):
        print('DELETE RECORD FROM COLLECTION ROUTE')

        user = User.objects.get(id=id1)
        
        serialized_user = UserCollection(user)

        print('SERIALIZED USER =>', serialized_user.data['collection'])

        if id2 in serialized_user.data['collection']:
            serialized_user.data['collection'].remove(id2)
            final = UserCollection(user, serialized_user.data, partial=True)
            final.is_valid(raise_exception=True)
            final.save()
            return Response(final.data)
        
        else: 
            return Response({ 'message': 'This record cannot be deleted because it is not in your collection.'})
        
class RemoveRecordFromWishlist(APIView):
    
    @exceptions
    def put(self, request, id1, id2):
        print('DELETE RECORD FROM WISHLIST ROUTE')

        user = User.objects.get(id=id1)
        
        serialized_user = UserWishlist(user)

        print('SERIALIZED USER =>', serialized_user.data['wishlist'])

        if id2 in serialized_user.data['wishlist']:
            serialized_user.data['wishlist'].remove(id2)
            final = UserWishlist(user, serialized_user.data, partial=True)
            final.is_valid(raise_exception=True)
            final.save()
            return Response(final.data)
        
        else: 
            return Response({ 'message': 'This record cannot be deleted because it is not in your wishlist.'})

class FollowUser(APIView):

  @exceptions
  def put(self, request, id1, id2):
      print('FOLLOW USER ROUTE HIT')
      
      print(id2)
      
      user1 = User.objects.get(id=id1)

      serialized_user = UserFollowing(user1)

      print('USER INFO =>', serialized_user.data)

      info = serialized_user.data
      print('INFO VARIABLE', info)

      if not id2 in info['following']:
        info['following'].append(id2)
        print('UPDATED INFO', info)
        final = UserFollowing(user1, info, partial=True)
        final.is_valid(raise_exception=True)
        final.save()
        return Response(final.data)
      
      else:
          return Response({ 'message': 'You are already following this user.' }) 

class UnfollowUser(APIView):
    
    @exceptions
    def put(self, request, id1, id2):
        print('UNFOLLOW ROUTE HIT')

        user = User.objects.get(id=id1)

        serialized_user = UserFollowing(user)

        info = serialized_user.data

        print('USER FOLLOWING =>', info['following'])

        if id2 in info['following']:
            info['following'].remove(id2)
            final = UserFollowing(user, info, partial=True)
            final.is_valid(raise_exception=True)
            final.save()
            return Response(final.data)
        else:
            return Response({ 'message': 'You have to follow a user before you unfollow them.' })