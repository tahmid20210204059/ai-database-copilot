from fastapi import Depends, HTTPException, status

from .jwt_handler import get_current_user

from ..models.user import User



def require_owner(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Allow only owner users.
    """


    if current_user.role != "owner":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Owner access required",
        )


    return current_user





def require_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Allow normal users.
    """


    if current_user.role != "user":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User access required",
        )


    return current_user