
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


from app.database import Session
from app.models.user import User
from app.crud.user import get_user_by_name
from app.schemas.user import UserSchema


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/access-token")

# oauth2_scheme = OAuth2PasswordRequestForm()

http_authorization = HTTPBearer()


# database session dependency
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
        db: Session = Depends(get_db),
        authorization: HTTPAuthorizationCredentials = Depends(http_authorization)
) -> User:
    """
    Get current user from request
    """
    user = get_user_by_name(db, authorization.credentials)
    if not user:
        raise HTTPException(status_code=403)
    return user


# def get_current_player(
#     current_user: models.User = Depends(get_current_user),
# ) -> models.User:
#     if not crud.user.is_active(current_user):
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
#
#
# def get_current_gm(
#     current_user: models.User = Depends(get_current_user),
# ) -> models.User:
#     if not crud.user.is_superuser(current_user):
#         raise HTTPException(
#             status_code=400, detail="The user doesn't have enough privileges"
#         )
#     return current_user



