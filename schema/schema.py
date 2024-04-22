from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class Locations(BaseModel):
    id: Optional[int] = Field(..., example=40)
    longitude : str = Field(..., example=80.03485)
    latitude : str = Field(..., example=53.40564)

class Categories(BaseModel):
    id: Optional[int] = Field(..., example=100)
    name: str = Field(..., example="Beach zone")

class Location_category_reviewed(BaseModel):
    id: Optional[int] = Field(..., example=1001)
    location_id: int = Field(..., example=40)
    category_id: int = Field(..., example=100)
    last_review_date : Optional[datetime] = None
    is_reviewed: bool = Field(default=False, example=False)
