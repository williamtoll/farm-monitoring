from pydantic import BaseModel


class Item(BaseModel):
    device_name: str
    date_exec: str
    zone: str
    
