from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied
from .models import Interest, Comment
from .serializers import UserSerializer, InterestSerializer, CommentSerializer

class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    user = User.objects.get(username=response.data['username'])
    refresh = RefreshToken.for_user(user)
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': response.data
    })

class LoginView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data
      })
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    user = User.objects.get(username=request.user)  # Fetch user profile
    refresh = RefreshToken.for_user(request.user) 
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserSerializer(user).data
    })

class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the P2g api home route!'}
    return Response(content)

class Post(generics.ListCreateAPIView):
    queryset= Interest.objects.all()
    serializer_class=InterestSerializer
    permission_classes= [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Interest.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset=Interest.objects.all()
    serializer_class=InterestSerializer
    lookup_field ='id'

    def get_queryset(self):
        user= self.request.user
        return Interest.objects.filter(user=user)

    def retrieve(self, request, *args, **kwargs):
        instance=self.get_object()
        serializer=self.get_serializer(instance)

        return Response({
            'interest': serializer.data
        })

    def perform_update(self, serializer):
        interest= self.get_object()
        if interest.user != self.request.user:
            raise PermissionDenied({'message':"You do not have permission to remove this post from the interest feeds."})
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied({"message": "You do not have permission to delete this post."})
        instance.delete()

class CommentListCreate(generics.ListCreateAPIView):
    serializer_class=CommentSerializer

    def get_queryset(self):
        interest_id= self.kwargs['interest_id']
        return Comment.objects.filter(interest_id=interest_id)
    
    def perform_create(self, serializer):
        interest_id = self.kwargs['interest_id']
        interest = Interest.objects.get(id=interest_id)
        serializer.save(interest=interest)

class CommentDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=CommentSerializer
    lookup_field= 'id'

    def get_queryset(self):
        interest_id= self.kwargs[interest_id]
        return Comment.objects.filter(interest_id=interest_id)