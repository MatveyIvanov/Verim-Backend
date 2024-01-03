import auth_pb2_grpc
from auth_pb2 import AuthResponse, User


class GRPCAuth(auth_pb2_grpc.AuthServicer):
    def auth(self, request, context):
        from utils.exceptions import CustomException
        from utils.middleware import authenticate_by_token

        try:
            return AuthResponse(
                user=User(id=authenticate_by_token(token=request.token).id)
            )
        except CustomException as e:
            return AuthResponse(user=User(id=-1), error_message=str(e))
