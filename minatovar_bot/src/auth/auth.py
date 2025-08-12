from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminUser, AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed

from src.admin.dal import AdminDAL
from src.auth.utils import verify_password
from src.db.session import async_session


class CoustomAuth(AuthProvider):
    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        if len(username) < 3:
            """Form data validation"""
            raise FormValidationError(
                {"username": "Ensure username has at least 03 characters"}
            )
        async with async_session() as db_session:
            admin_dal = AdminDAL(db_session=db_session)
            admin = await admin_dal.get_admin_by_username(username=username)
            if admin and verify_password(password, admin.hashed_password):
                """Save `username` in session"""
                request.session.update({"username": username})
                return response

            raise LoginFailed("Invalid username or password")

    async def is_authenticated(self, request) -> bool:
        async with async_session() as db_session:
            username = request.session.get("username", None)
            admin_dal = AdminDAL(db_session=db_session)
            admin = await admin_dal.get_admin_by_username(username=username)
            if admin:
                """
                Save current `user` object in the request state. Can be used later
                to restrict access to connected user.
                """
                request.state.user = request.session["username"]
                return True

            return False

    def get_admin_user(self, request: Request) -> AdminUser:
        user = request.state.user  # Retrieve current user
        return AdminUser(username=user)

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response
