from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .models import FriendRequest, Friendship
from .serializers import UserSerializer, FriendRequestSerializer, FriendSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

User = get_user_model()

class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


@csrf_exempt
@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        data = request.data
        serializer = UserSerializer().create_user(data)
        if serializer:
            return Response("We have successfully saved data into database", status=201)
        return Response(serializer.error, status=400)

class GetUserDetails(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):

        email = request.query_params.get("email", None)
        name = request.query_params.get("name", None)
        try:
            if email:
                serializer = UserSerializer().get_user_by_email(email)
                return Response({"name": serializer.username, "email": serializer.email}, status=200)
            elif name:
                serializer = UserSerializer().get_user_by_name(name)
                return Response({"details": serializer}, status=200)
            else:
                return Response("Bad Request", status=400)
        except Exception as err:
            raise APIException(detail=err, code=500)


@csrf_exempt
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        data = request.data
        try:
            serializer = UserSerializer().check_user_login(data.get('email'), data.get('password'))
            if serializer:
                return Response({"details": "User has been logged in successfully"}, status=200)
            else:
                return Response("User Not Found. Please check credentials and try again.", status=401)
        except Exception as err:
            return APIException(detail=err, code=500)

class SendFriendRequestView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        username = request.data.get("sender_username")
        user = User.objects.get(username=username)
        receiver_email = request.data.get('receiver_email')

        try:
            receiver = User.objects.get(email=receiver_email)
        except User.DoesNotExist:
            return Response({'detail': 'Receiver not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Rate limiting
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        recent_requests = FriendRequest.objects.filter(sender=user, timestamp__gte=one_minute_ago).count()
        if recent_requests >= 3:
            return Response({'detail': 'You can only send 3 friend requests per minute.'},
                            status=status.HTTP_429_TOO_MANY_REQUESTS)
        # Creating friend request
        friend_request, created = FriendRequest.objects.get_or_create(sender=user, receiver=receiver, status="pending")
        if not created:
            return Response({'detail': 'Friend request already sent.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_201_CREATED)


class ManageFriendRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')  #provide a user for which we want to manage the friend request
        user = User.objects.get(username=username)
        request_id = request.data.get('request_id')
        action = request.data.get('action')
        friend_request = FriendRequest.objects.get(id=request_id)

        if friend_request.receiver != user:
            return Response({'detail': 'Not authorized to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        if(friend_request.status == 'accepted'):
            return Response({'detail':"duplicate request"}, status= status.HTTP_409_CONFLICT)

        if action == 'accept':
            friend_request.status = 'accepted'
            Friendship.objects.create(user1=friend_request.sender, user2=friend_request.receiver)
        elif action == 'reject':
            friend_request.status = 'rejected'
        else:
            return Response({'detail': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)

        friend_request.save()
        return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_200_OK)


class ListFriendsView(APIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        username = request.data.get('username')
        user = User.objects.get(username=username)
        friendships = Friendship.objects.filter(Q(user1=user) | Q(user2=user))
        friend_ids = [f.user1.id if f.user2 == user else f.user2.id for f in friendships]
        friends = User.objects.filter(id__in=friend_ids)
        serializer = FriendSerializer(friends, many=True)
        if(serializer.data):
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("No friends", status=status.HTTP_204_NO_CONTENT)

class ListPendingFriendRequestsView(APIView):

    # permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.data.get("username")
        user = User.objects.get(username=username)
        friend_request = FriendRequest.objects.filter(receiver=user, status='pending')
        serializer = FriendRequestSerializer(friend_request, many=True)

        if(serializer.data):
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("No pending request", status=status.HTTP_204_NO_CONTENT)



