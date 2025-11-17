from pydantic import BaseModel, Field
from typing import Optional, List
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class NewsArticle(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    title: str
    text: str
    summary: Optional[str] = None
    url: str
    source: str
    published_date: Optional[str] = None
    category: Optional[str] = None
    sentiment: Optional[dict] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

class SummarizeRequest(BaseModel):
    text: str

class CategorizeRequest(BaseModel):
    text: str

class SentimentRequest(BaseModel):
    text: str
