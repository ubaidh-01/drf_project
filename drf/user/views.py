from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework import generics

from rest_framework.permissions import IsAuthenticated

from.serializers import RegisterSerializer, LoginSerializer, PostSerializer, UserSerializer

from.models import User
from .models import Post
from rest_framework.generics import RetrieveUpdateAPIView

from rest_framework_simplejwt.authentication import JWTAuthentication

            
# REGISTER VIEW
class RegisterView(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = RegisterSerializer(data = data)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message' : 'Something went wrong',
                },
                     status = status.HTTP_400_BAD_REQUEST )
            
            serializer.save()        
            return Response({
                'data': {},
                'message' : 'Your Account is created successfully !',
                },
                 status = status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                    {
                    'data': {},
                    'message' : 'Something went wrong',
                    },
                     status = status.HTTP_400_BAD_REQUEST )
        

# =========================================================================================================================================
                  

# LOGIN VIEW
class LoginView(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data = data)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message' : 'something went wrong',
                },
                     status = status.HTTP_400_BAD_REQUEST )
            responce = serializer.get_jwt_token(serializer.data)
            return Response(responce,status=status.HTTP_200_OK )
        
        except Exception as e:
            print(e)
            return Response(
                    {
                    'data': {},
                    'message' : 'Something went wrong',
                    },
                     status = status.HTTP_400_BAD_REQUEST )
            

# ==============================================================================================================================================
     
# USER VIEW
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all() 

    @action(detail=False, methods=['GET', 'PUT', 'PATCH'], url_path='current-user')
    def current_user(self, request, *args, **kwargs):
        user = self.request.user

        if request.method in ('PUT', 'PATCH'):
           
            if user.pk != request.user.pk:
                return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
                'data': serializer.data,
                'message' : 'Post Updated successfully !',
                },
                 status = status.HTTP_200_OK)



# PUBLIC USER VIEW
class PublicUserListView(generics.ListAPIView):
    queryset = User.objects.all() 
    serializer_class = UserSerializer


# ================================================================================================

class PostView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    
    def get(self, request):
        try:
            posts = Post.objects.filter(user = request.user)
            serializer = PostSerializer(posts, many=True)
            return Response({
                'data': serializer.data,
                'message' : 'Post fetched successfully !',
                },
                 status = status.HTTP_200_OK)
        except Exception as e:
            return Response(
                    {
                    'data': {},
                    'message' : 'Something went wrong',
                    },
                     status = status.HTTP_400_BAD_REQUEST )

    # ----------------------------------------------------------------------------------------------------
    def post(self, request):
        try:
            data = request.data
            data['user'] = request.user.id
            serializer = PostSerializer(data = data)

            if not serializer.is_valid():
                return Response(
                    {
                    'data': serializer.errors,
                    'message' : 'Something went wrong',
                    },
                     status = status.HTTP_400_BAD_REQUEST )
            
            serializer.save()
            return Response({
                'data': serializer.data,
                'message' : 'Post created successfully !',
                },
                 status = status.HTTP_201_CREATED)


        except Exception as e:
            print(e)
            return Response(
                    {
                    'data': {},
                    'message' : 'Something went wrong',
                    },
                     status = status.HTTP_400_BAD_REQUEST )
        
    # -----------------------------------------------------------------------------------------------
    def patch(self, request):
        try:
            data = request.data
            post = Post.objects.filter(uid = data.get('uid'))
            if not post.exists():
                return Response(
                    {
                    'data': {},
                    'message' : 'This post does not exist',
                    },
                     status = status.HTTP_400_BAD_REQUEST )

            if request.user != post[0].user:
                return Response(
                    {
                    'data': {},
                    'message' : 'You are not authorized to edit that !',
                    },
                     status = status.HTTP_400_BAD_REQUEST )
            
            serializer = PostSerializer(post[0], data=data, partial = True)
            if not serializer.is_valid():
                return Response(
                    {
                    'data': serializer.errors,
                    'message' : 'Something went wrong',
                    },
                     status = status.HTTP_400_BAD_REQUEST )
            serializer.save()
            return Response({
                'data': serializer.data,
                'message' : 'Post Updated successfully !',
                },
                 status = status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(
                    {
                    'data': {},
                    'message' : 'Something went wrong',
                    },
                     status = status.HTTP_400_BAD_REQUEST )
        
    # ---------------------------------------------------------------------------------------------

    def delete(self, request):
        try:
            data = request.data
            post = Post.objects.filter(uid = data.get('uid'))
            if not post.exists():
                return Response(
                    {
                    'data': {},
                    'message' : 'This post does not exist',
                    },
                     status = status.HTTP_400_BAD_REQUEST )

            if request.user != post[0].user:
                return Response(
                    {
                    'data': {},
                    'message' : 'You are not authorized to edit that !',
                    },
                     status = status.HTTP_400_BAD_REQUEST )
            post[0].delete()
            return Response(
                    {
                    'data': {},
                    'message' : 'Post deleted successfully !',
                    },
                     status = status.HTTP_200_OK )
        
        except Exception as e:
            return Response(
                    {
                    'data': {},
                    'message' : 'Something went wrong',
                    },
                     status = status.HTTP_400_BAD_REQUEST )

