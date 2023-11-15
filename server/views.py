# Import necessary modules and classes from Django REST framework
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Category, Server, Channel
from .serializers import ServerSerializer
from django.db.models import Count
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from .schema import server_list_docs


class ServerListView(viewsets.ViewSet):
    """
    A view set for handling server list-related operations.

    Attributes:
        queryset (QuerySet): The default queryset including all Server objects.
    """

    queryset = Server.objects.all()

    @server_list_docs
    def list(self, request):
        """
        Handles GET requests for server lists.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The serialized data and additional information.
        """
        # Extract query parameters from the request
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = request.query_params.get("by_user") == "true"
        by_serverid = request.query_params.get("by_serverid")
        with_num_members = request.query_params.get("with_num_members") == "true"

        # Check if authentication is required and not provided
        # if by_user or by_serverid and not request.user.is_authenticated:
        #     raise AuthenticationFailed(
        #         detail="Authentication credentials were not provided."
        #     )

        # Apply filters based on query parameters
        if category:
            # Filter servers by category name
            self.queryset = self.queryset.filter(category__name=category)

        if by_user:
            if by_user and request.user.is_authenticated:
                # Filter servers by the requesting user
                user_id = request.user.id
                self.queryset = self.queryset.filter(member=user_id)
            else:
                raise ValidationError(detail="Invalid filter combination.")

        if with_num_members:
            # Annotate queryset with the count of members
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        if qty:
            # Limit the queryset to a specified quantity
            self.queryset = self.queryset[: int(qty)]

        if by_serverid:
            try:
                # Filter servers by the provided server ID
                self.queryset = self.queryset.filter(id=by_serverid)
                # Raise ValidationError if the server with the given ID doesn't exist
                if not self.queryset.exists():
                    raise ValidationError(
                        {
                            "status": False,
                            "message": "Server Not Found",
                            "detail": f"Server with id = {by_serverid} does not exist",
                        }
                    )
            except ValueError:
                # Raise ValidationError for an invalid server ID format
                raise ValidationError({"detail": "Invalid server ID provided."})

        # Serialize the queryset using ServerSerializer
        serializer = ServerSerializer(
            self.queryset, many=True, context={"num_members": with_num_members}
        )

        # Return a Response with the serialized data and additional information
        return Response(
            {
                "status": True,
                "message": "successfully done",
                "count": len(serializer.data),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK
        )
