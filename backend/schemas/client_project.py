from pydantic import BaseModel
from typing import Optional, List
from datetime import date

# Project File Schema
class ProjectFileResponse(BaseModel):
    """Schema for project file response"""
    id: str
    filename: str
    file_path: str
    uploaded_at: str
    uploaded_by: str

# Client Project Schemas
class ClientProjectCreate(BaseModel):
    """Schema for creating a new client project"""
    name: str
    client_id: str
    description: Optional[str] = None
    status: str = "pending"
    progress: int = 0
    expected_delivery: Optional[date] = None
    notes: Optional[str] = None

class ClientProjectUpdate(BaseModel):
    """Schema for updating a client project"""
    name: Optional[str] = None
    client_id: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    progress: Optional[int] = None
    expected_delivery: Optional[date] = None
    notes: Optional[str] = None

class ClientProjectResponse(BaseModel):
    """Schema for client project response"""
    id: str
    name: str
    client_id: str
    description: Optional[str] = None
    status: str
    progress: int
    expected_delivery: Optional[str] = None
    notes: Optional[str] = None
    files: List[ProjectFileResponse] = []
    created_at: str
    updated_at: Optional[str] = None

class FileUploadResponse(BaseModel):
    """Schema for file upload response"""
    id: str
    filename: str
    message: str
