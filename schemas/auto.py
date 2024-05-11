from pydantic import UUID4, BaseModel


class UpdateTagResponse(BaseModel):
    id: UUID4


class TagSchema(BaseModel):
    id: UUID4
    tag: str


class TagForListSchema(TagSchema):
    max_use: int


class GetTagsResponse(BaseModel):
    tags: list[TagForListSchema]
