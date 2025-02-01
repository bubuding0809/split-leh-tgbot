import aiohttp
from pydantic import BaseModel, Field
from env import env
from typing import Optional, Union


class User(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str] = Field(default=None)
    username: Optional[str] = Field(default=None)
    created_at: str
    updated_at: str


class ApiResult(BaseModel):
    status: int
    message: str


class GetUserPayload(BaseModel):
    user_id: int


class GetUserResult(ApiResult):
    user: Optional[User] = Field(default=None)


class CreateChatPayload(BaseModel):
    chat_id: int
    chat_title: str
    chat_type: str
    chat_photo_url: Optional[str] = Field(default=None)


class CreateChatResult(ApiResult):
    pass


class CreateUserPayload(BaseModel):
    user_id: int
    first_name: str
    last_name: Optional[str] = Field(default=None)
    username: Optional[str] = Field(default=None)


class CreateUserResult(ApiResult):
    pass


class AddMemberPayload(BaseModel):
    chat_id: int
    user_id: int


class AddMemberResult(ApiResult):
    pass


class Api:
    def __init__(self):
        self.default_headers = {"Authorization": f"Bearer {env.API_KEY}"}
        self.aio_session = aiohttp.ClientSession(
            base_url=env.API_BASE_URL,
            headers=self.default_headers,
        )

    async def get_user(
        self, payload: GetUserPayload
    ) -> Union[GetUserResult, Exception]:
        try:
            async with self.aio_session.get(f"user/{payload.user_id}") as response:
                response.raise_for_status()

                data = await response.json()
                userData = data.get("data")

                return GetUserResult(
                    user=User(
                        id=userData.get("id"),
                        first_name=userData.get("firstName"),
                        last_name=userData.get("lastName"),
                        username=userData.get("username"),
                        created_at=userData.get("createdAt"),
                        updated_at=userData.get("updatedAt"),
                    ),
                    status=response.status,
                    message=data.get("message"),
                )
        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                return GetUserResult(
                    user=None,
                    status=e.status,
                    message="User not found",
                )
            return e
        except Exception as e:
            return e

    async def create_user(
        self, payload: CreateUserPayload
    ) -> Union[CreateUserResult, Exception]:
        try:
            async with self.aio_session.post(
                "user",
                json=payload.model_dump(),
            ) as response:
                response.raise_for_status()

                data = await response.json()

                return CreateUserResult(
                    status=response.status,
                    message=data.get("message"),
                )
        except Exception as e:
            return e

    async def create_chat(
        self, payload: CreateChatPayload
    ) -> Union[CreateChatResult, Exception]:
        try:
            async with self.aio_session.post(
                "chat",
                json=payload.model_dump(),
            ) as response:
                response.raise_for_status()
                res = await response.json()

                return CreateChatResult(
                    status=response.status,
                    message=res.get("message"),
                )
        except Exception as e:
            return e

    async def add_member(
        self, payload: AddMemberPayload
    ) -> Union[AddMemberResult, Exception]:
        try:
            async with self.aio_session.patch(
                f"chat/{payload.chat_id}/members",
                json={
                    "user_id": payload.user_id,
                },
            ) as response:
                response.raise_for_status()
                res = await response.json()

                return AddMemberResult(
                    status=response.status,
                    message=res.get("message"),
                )
        except Exception as e:
            return e

    async def clean_up(self):
        await self.aio_session.close()
