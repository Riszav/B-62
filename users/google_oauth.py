import requests
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from users.serializers import OAuthCodeSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model


User = get_user_model()


class GoogleLoginAPIView(CreateAPIView):
    serializer_class = OAuthCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data["code"]

        token_response = requests.post(
            url="https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": "981803348149-4qst1ghhn23r5bdau5ot0q03tbeq000q.apps.googleusercontent.com",
                "client_secret": "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",
                "redirect_uri": "http://localhost:8000/api/v1/users/google-login",
                "grant_type": "authorization_code"
            }
        )

        token_data = token_response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            return Response({"error": f"Invalid access token: {token_data}"})

        user_info = requests.get(
            url="https://www.googleapis.com/oauth2/v3/userinfo",
            params={"alt": "json"},
            headers={"Authorization": f"Bearer {access_token}"}
        ).json()

        print(f"USER_INFO: {user_info}")

        email = user_info["email"]

        user, created = User.objects.get_or_create(
            email=email,
        )

        refresh = RefreshToken.for_user(user)
        refresh["email"] = user.email

        return Response(
            {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            }
        )
