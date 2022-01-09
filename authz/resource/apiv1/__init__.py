from authz.authz import apiv1 as api
from authz.resource.apiv1.user import UserResource

api.add_resource(
    UserResource,
    "/users",
    method=["GET","POST"],
    endpoint="users"
)

api.add_resource(
    UserResource,
    "/users/<userid>",
    method=["GET","PATCH","DELETE"],
    endpoint="user"
)

