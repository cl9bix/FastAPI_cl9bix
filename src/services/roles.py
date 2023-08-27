from typing import List

from fastapi import Request, Depends, HTTPException, status

from src.database.models import Role, User
from src.services.auth import auth_service


class RoleAccess:
    def __init__(self, allowed_roles: List[Role]):
        """
        The __init__ function is called when the class is instantiated.
        It allows us to pass in a list of allowed roles, which we can then use to check if the user has access.
        
        :param self: Represent the instance of the class
        :param allowed_roles: List[Role]: Define the allowed roles for a user
        :return: Nothing
        :doc-author: Trelent
        """
        self.allowed_roles = allowed_roles

    async def __call__(self, request: Request, user: User = Depends(auth_service.get_current_user)):
        """
        The __call__ function is a decorator that takes in the request and user as parameters.
        It then checks if the user's role is in the list of allowed roles for this endpoint.
        If it isn't, an HTTPException with status code 403 (Forbidden) will be raised.
        
        :param self: Access the class attributes
        :param request: Request: Get the request object
        :param user: User: Get the current user
        :return: A response object, which is a json-serializable object
        :doc-author: Trelent
        """
        print(user.role)
        print(self.allowed_roles)
        if user.role not in self.allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation forbidden")