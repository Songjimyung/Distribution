from rest_framework.views import APIView
from chat.models import Room, Message
from users.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from collections import Counter


class RoomView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        작성자 : 박지홍
        내용 : 채팅을위한 Room을 만드는 기능.
            - 이미 같은 대상과의 채팅방이 존재 할 경우 만들어진 방번호를 반환한다.
        최초 작성일 : 2023.06.06
        업데이트 일자 : 2023.06.15
        #06.15 : 1:1 통신만 존재함으로 인해 기존의 N:N 통신 기반 함수를 덜어냄.
        """
        counselor = User.objects.filter(is_admin=True).first()
        find_room_q = Room.objects.filter(advisee=request.user).first()
        if find_room_q:
            return Response(find_room_q.id, status=status.HTTP_200_OK)

        room = Room.objects.create(advisee=request.user, counselor=counselor)
        return Response(room.id, status=status.HTTP_201_CREATED)
