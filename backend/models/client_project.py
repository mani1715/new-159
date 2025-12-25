from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
import uuid

class ProjectFile(BaseModel):
    """File attached to a project"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    filename: str
    file_path: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    uploaded_by: str  # Admin ID

class ClientProject(BaseModel):
    """Project assigned to a client"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    client_id: str
    description: Optional[str] = None
    status: str = "pending"  # pending, in_progress, review, completed
    progress: int = 0  # 0-100
    expected_delivery: Optional[date] = None
    notes: Optional[str] = None  # Admin notes visible to client
    files: List[ProjectFile] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str  # Admin ID
    updated_at: Optional[datetime] = None
