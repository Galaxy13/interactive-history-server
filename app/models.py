from pydantic import BaseModel, Field
from typing import Optional, List, Union
from bson import ObjectId


# from enum import Enum
#
# class Gender(str, Enum):
#     MALE = 'male'
#     FEMALE = 'female'
#
# class Role(str, Enum):
#     admin = 'admin'
#     user = 'user'
#     student = 'student'

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Inavalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class Image(BaseModel):
    # id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    type: str = 'image'
    image_link: str = Field(...)
    image_pos: List[int] = Field(...)

    # class Config:
    #     json_encoders = {ObjectId: str}


class Text(BaseModel):
    # id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    type: str = 'text'
    text: str = Field(...)
    text_pos: List[int] = Field(...)

    # class Config:
    #     json_encoders = {ObjectId: str}


class Slide(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    lesson_id: Optional[PyObjectId] = Field(default_factory=PyObjectId)
    slide_number: int = Field(...)
    objects: List[Union[Image, Text]] = Field(...)

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


class Lesson(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    lesson_name: str = Field(...)
    lesson_class: int = Field(...)
    class_id: Optional[PyObjectId] = Field(default_factory=PyObjectId)

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


class Class(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    class_name: Optional[str] = Field(...)
    class_number: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
