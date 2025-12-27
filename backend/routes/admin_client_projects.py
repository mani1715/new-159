from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File
from typing import List
from schemas.client_project import ClientProjectCreate, ClientProjectUpdate, ClientProjectResponse, FileUploadResponse, ProjectFileResponse
from database import client_projects_collection, clients_collection
from auth.admin_auth import get_current_admin
from models.client_project import ClientProject, ProjectFile
from datetime import datetime
import os
import uuid
import shutil

router = APIRouter(prefix="/admin/client-projects", tags=["admin-client-projects"])

# Directory for storing project files
UPLOAD_DIR = "/app/backend/uploads/client_projects"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/", response_model=List[ClientProjectResponse])
async def get_all_projects(admin = Depends(get_current_admin)):
    """Get all client projects (Admin only)"""
    projects = []
    async for project_doc in client_projects_collection.find():
        projects.append(ClientProjectResponse(
            id=project_doc['id'],
            name=project_doc['name'],
            client_id=project_doc['client_id'],
            description=project_doc.get('description'),
            status=project_doc['status'],
            progress=project_doc['progress'],
            expected_delivery=str(project_doc['expected_delivery']) if project_doc.get('expected_delivery') else None,
            notes=project_doc.get('notes'),
            files=[
                ProjectFileResponse(
                    id=f['id'],
                    filename=f['filename'],
                    file_path=f['file_path'],
                    uploaded_at=f['uploaded_at'] if isinstance(f['uploaded_at'], str) else f['uploaded_at'].isoformat(),
                    uploaded_by=f['uploaded_by']
                ) for f in project_doc.get('files', [])
            ],
            created_at=project_doc['created_at'] if isinstance(project_doc['created_at'], str) else project_doc['created_at'].isoformat(),
            updated_at=project_doc.get('updated_at')
        ))
    return projects

@router.get("/{project_id}", response_model=ClientProjectResponse)
async def get_project(project_id: str, admin = Depends(get_current_admin)):
    """Get a specific client project (Admin only)"""
    project_doc = await client_projects_collection.find_one({"id": project_id})
    
    if not project_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return ClientProjectResponse(
        id=project_doc['id'],
        name=project_doc['name'],
        client_id=project_doc['client_id'],
        description=project_doc.get('description'),
        status=project_doc['status'],
        progress=project_doc['progress'],
        expected_delivery=str(project_doc['expected_delivery']) if project_doc.get('expected_delivery') else None,
        notes=project_doc.get('notes'),
        files=[
            ProjectFileResponse(
                id=f['id'],
                filename=f['filename'],
                file_path=f['file_path'],
                uploaded_at=f['uploaded_at'] if isinstance(f['uploaded_at'], str) else f['uploaded_at'].isoformat(),
                uploaded_by=f['uploaded_by']
            ) for f in project_doc.get('files', [])
        ],
        created_at=project_doc['created_at'] if isinstance(project_doc['created_at'], str) else project_doc['created_at'].isoformat(),
        updated_at=project_doc.get('updated_at')
    )

@router.post("/", response_model=ClientProjectResponse)
async def create_project(project_data: ClientProjectCreate, admin = Depends(get_current_admin)):
    """Create a new client project (Admin only)"""
    # Verify client exists
    client = await clients_collection.find_one({"id": project_data.client_id})
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # Create project
    project = ClientProject(
        name=project_data.name,
        client_id=project_data.client_id,
        description=project_data.description,
        status=project_data.status,
        progress=project_data.progress,
        expected_delivery=project_data.expected_delivery,
        notes=project_data.notes,
        created_by=admin["id"]
    )
    
    project_dict = project.model_dump()
    project_dict['created_at'] = project_dict['created_at'].isoformat()
    if project_dict['expected_delivery']:
        project_dict['expected_delivery'] = project_dict['expected_delivery'].isoformat()
    
    await client_projects_collection.insert_one(project_dict)
    
    return ClientProjectResponse(
        id=project.id,
        name=project.name,
        client_id=project.client_id,
        description=project.description,
        status=project.status,
        progress=project.progress,
        expected_delivery=str(project.expected_delivery) if project.expected_delivery else None,
        notes=project.notes,
        files=[],
        created_at=project_dict['created_at'],
        updated_at=None
    )

@router.put("/{project_id}", response_model=ClientProjectResponse)
async def update_project(project_id: str, project_data: ClientProjectUpdate, admin = Depends(get_current_admin)):
    """Update a client project (Admin only)"""
    project_doc = await client_projects_collection.find_one({"id": project_id})
    
    if not project_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Prepare update data
    update_data = {}
    if project_data.name is not None:
        update_data['name'] = project_data.name
    if project_data.client_id is not None:
        # Verify new client exists
        client = await clients_collection.find_one({"id": project_data.client_id})
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )
        update_data['client_id'] = project_data.client_id
    if project_data.description is not None:
        update_data['description'] = project_data.description
    if project_data.status is not None:
        update_data['status'] = project_data.status
    if project_data.progress is not None:
        update_data['progress'] = max(0, min(100, project_data.progress))  # Clamp 0-100
    if project_data.expected_delivery is not None:
        update_data['expected_delivery'] = project_data.expected_delivery.isoformat()
    if project_data.notes is not None:
        update_data['notes'] = project_data.notes
    
    update_data['updated_at'] = datetime.utcnow().isoformat()
    
    await client_projects_collection.update_one(
        {"id": project_id},
        {"$set": update_data}
    )
    
    # Fetch updated project
    updated_project = await client_projects_collection.find_one({"id": project_id})
    
    return ClientProjectResponse(
        id=updated_project['id'],
        name=updated_project['name'],
        client_id=updated_project['client_id'],
        description=updated_project.get('description'),
        status=updated_project['status'],
        progress=updated_project['progress'],
        expected_delivery=str(updated_project['expected_delivery']) if updated_project.get('expected_delivery') else None,
        notes=updated_project.get('notes'),
        files=[
            ProjectFileResponse(
                id=f['id'],
                filename=f['filename'],
                file_path=f['file_path'],
                uploaded_at=f['uploaded_at'] if isinstance(f['uploaded_at'], str) else f['uploaded_at'].isoformat(),
                uploaded_by=f['uploaded_by']
            ) for f in updated_project.get('files', [])
        ],
        created_at=updated_project['created_at'] if isinstance(updated_project['created_at'], str) else updated_project['created_at'].isoformat(),
        updated_at=updated_project.get('updated_at')
    )

@router.delete("/{project_id}")
async def delete_project(project_id: str, admin = Depends(get_current_admin)):
    """Delete a client project (Admin only)"""
    # Get project to delete associated files
    project_doc = await client_projects_collection.find_one({"id": project_id})
    
    if project_doc:
        # Delete associated files from filesystem
        for file_info in project_doc.get('files', []):
            file_path = file_info.get('file_path')
            if file_path and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception:
                    pass  # Continue even if file deletion fails
    
    result = await client_projects_collection.delete_one({"id": project_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return {"message": "Project deleted successfully"}

@router.post("/{project_id}/files", response_model=FileUploadResponse)
async def upload_project_file(
    project_id: str,
    file: UploadFile = File(...),
    admin = Depends(get_current_admin)
):
    """Upload a file to a project (Admin only)"""
    # Verify project exists
    project_doc = await client_projects_collection.find_one({"id": project_id})
    if not project_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Create project-specific directory
    project_dir = os.path.join(UPLOAD_DIR, project_id)
    os.makedirs(project_dir, exist_ok=True)
    
    # Generate unique filename
    file_id = str(uuid.uuid4())
    file_extension = os.path.splitext(file.filename)[1]
    safe_filename = f"{file_id}{file_extension}"
    file_path = os.path.join(project_dir, safe_filename)
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}"
        )
    
    # Create file metadata
    project_file = ProjectFile(
        id=file_id,
        filename=file.filename,
        file_path=file_path,
        uploaded_by=admin["id"]
    )
    
    file_dict = project_file.model_dump()
    file_dict['uploaded_at'] = file_dict['uploaded_at'].isoformat()
    
    # Add file to project
    await client_projects_collection.update_one(
        {"id": project_id},
        {"$push": {"files": file_dict}}
    )
    
    return FileUploadResponse(
        id=file_id,
        filename=file.filename,
        message="File uploaded successfully"
    )

@router.delete("/{project_id}/files/{file_id}")
async def delete_project_file(
    project_id: str,
    file_id: str,
    admin = Depends(get_current_admin)
):
    """Delete a file from a project (Admin only)"""
    # Get project
    project_doc = await client_projects_collection.find_one({"id": project_id})
    if not project_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Find file in project
    file_to_delete = None
    for file_info in project_doc.get('files', []):
        if file_info['id'] == file_id:
            file_to_delete = file_info
            break
    
    if not file_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Delete file from filesystem
    file_path = file_to_delete['file_path']
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete file: {str(e)}"
            )
    
    # Remove file from project
    await client_projects_collection.update_one(
        {"id": project_id},
        {"$pull": {"files": {"id": file_id}}}
    )
    
    return {"message": "File deleted successfully"}
