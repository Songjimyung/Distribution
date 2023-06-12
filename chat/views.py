from rest_framework.views import APIView
from chat.models import Room, RoomJoin, Message
from users.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from collections import Counter


class RoomView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        작성자 : 박지홍
        내용 : 유저가 속해있는 채팅방을 조회하는 기능
        최초 작성일 : 2023.06.06
        업데이트 일자 :
        """
        user_chat_room = RoomJoin.objects.filter(user_id=request.user.id)
        room_info = {}
        for chat_room in user_chat_room:
            room_id = chat_room.room_id.id
            chat_user_list = RoomJoin.objects.filter(room_id=room_id)

            room_user_list = []
            for user_list in chat_user_list:
                username = user_list.user_id.email
                room_user_list.append(username)

            room_info[room_id] = room_user_list
        if room_info == {}:
            room_info = None
        return Response(room_info, status=status.HTTP_200_OK)

    def post(self, request):
        """
        작성자 : 박지홍
        내용 : 채팅을위한 Room을 만드는 기능.
            - 이미 같은 대상과의 채팅방이 존재 할 경우 만들어진 방번호를 반환한다.
        최초 작성일 : 2023.06.06
        업데이트 일자 :
        """
        user = User.objects.get(id=request.user.id)
        admin = User.objects.filter(is_admin=True).first()
        find_room_q = RoomJoin.objects.filter(user_id__in=[user.id, admin.id])

        find_room_list = []
        for find_room in find_room_q:
            find_room_list.append(find_room.room_id)

        result = Counter(find_room_list)
        for key, value in result.items():
            if value >= 2:
                return Response(key.id, status=status.HTTP_200_OK)

        room = Room.objects.create()
        RoomJoin.objects.create(user_id=user, room_id=room)
        RoomJoin.objects.create(user_id=admin, room_id=room)

        return Response(room.id, status=status.HTTP_201_CREATED)


class ChatRoom(APIView):
    def get(self, request):
        """
        작성자 : 박지홍
        내용 : 특정 채팅방에 대한 정보를 출력하는 기능
        최초 작성일 : 2023.06.06
        업데이트 일자 :
        """
        room_id = request.data.get("room_id", None)
        try:
            check_room = RoomJoin.objects.get(user_id=request.user.id, room_id=room_id)
            message = Message.objects.filter(room_id=room_id)

            return Response(message, status=status.HTTP_200_OK)

        except:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)
