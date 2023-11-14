from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Category, Server, Channel
from .serializers import ServerSerializer


class ServerListView(viewsets.ViewSet):
    queryset = Server.objects.all()

    def list(self, request):
        category_id = request.query_params.get("category")

        if category_id:
            try:
                category = Category.objects.get(id=category_id)
                self.queryset = self.queryset.filter(category=category)
            except Category.DoesNotExist:
                return Response(
                    {"status": False, "message": "Category not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

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