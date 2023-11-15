from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Category, Server, Channel
from .serializers import ServerSerializer
from rest_framework.exceptions import ValidationError, AuthenticationFailed


class ServerListView(viewsets.ViewSet):
    queryset = Server.objects.all()

    def list(self, request):
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = request.query_params.get("by_user") == "true"
        by_serverid = request.query_params.get("by_serverid")

        if by_user or by_serverid and not request.user.is_authenticated:
            raise AuthenticationFailed(
                detail="Authentication credentials were not provided."
            )

        if category:
           self.queryset = self.queryset.filter(category__name=category)

        if by_user:
            user_id = request.user.id
            self.queryset = self.queryset.filter(member=user_id)

        if qty:
            self.queryset = self.queryset[: int(qty)]

        if by_serverid:
            try:
                self.queryset = self.queryset.filter(id=by_serverid)
                if not self.queryset.exists():
                    raise ValidationError(
                        {
                            "status":False,
                            "message":"Server Not Found",
                            "detail": f"Server with id = {by_serverid} does not exist",
                        })
            except ValueError:
                raise ValidationError({"detail": "Invalid server ID provided."})

        serializer = ServerSerializer(self.queryset, many=True)
        return Response(
            {
                "status": True,
                "message": "successfully done",
                "count": len(serializer.data),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK
        )