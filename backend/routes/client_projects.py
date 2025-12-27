from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import FileResponse
from typing import List
from schemas.client_project import ClientProjectResponse, ProjectFileResponse
from database import client_projects_collection
from auth.client_auth import get_current_client
import os

router = APIRouter(prefix="/client/projects", tags=["client-projects"])

@router.get("/", response_model=List[ClientProjectResponse])
async def get_my_projects(client = Depends(get_current_client)):
    """Get all projects assigned to the current client"""
    projects = []
    async for project_doc in client_projects_collection.find({"client_id": client["id"]}):
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
async def get_project(project_id: str, client = Depends(get_current_client)):
    """Get a specific project (only if assigned to current client)"""
    project_doc = await client_projects_collection.find_one({
        "id": project_id,
        "client_id": client["id"]
    })
    
    if not project_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or not assigned to you"
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

@router.get("/{project_id}/files/{file_id}/download")
async def download_project_file(
    project_id: str,
    file_id: str,
    client = Depends(get_current_client)
):
    """Download a file from a project (only if project is assigned to current client)"""
    # Verify project belongs to client
    project_doc = await client_projects_collection.find_one({
        "id": project_id,
        "client_id": client["id"]
    })
    
    if not project_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or not assigned to you"
        )
    
    # Find file in project
    file_info = None
    for f in project_doc.get('files', []):
        if f['id'] == file_id:
            file_info = f
            break
    
    if not file_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    file_path = file_info['file_path']
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found on server"
        )
    
    return FileResponse(
        path=file_path,
        filename=file_info['filename'],
        media_type='application/octet-stream'
    )
