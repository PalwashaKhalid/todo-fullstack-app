from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import datetime
from src.database import get_db
from src.models.task import Task, TaskCreate, TaskUpdate, TaskStatusUpdate, TaskResponse
from src.models.user import User
from src.auth.dependencies import get_current_user

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new task for the authenticated user

    Args:
        task_data: Task creation data (title, description)
        current_user: Authenticated user from JWT token
        db: Database session

    Returns:
        Created task information

    Raises:
        HTTPException: 400 if validation fails
    """
    # Validate title is not empty
    if not task_data.title or not task_data.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title cannot be empty"
        )

    # Validate title length
    if len(task_data.title) > 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title must be 200 characters or less"
        )

    # Validate description length if provided
    if task_data.description and len(task_data.description) > 2000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task description must be 2000 characters or less"
        )

    # Create task associated with current user
    new_task = Task(
        user_id=current_user.id,
        title=task_data.title.strip(),
        description=task_data.description.strip() if task_data.description else None,
        completed=False
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "success": True,
        "data": TaskResponse(
            id=new_task.id,
            user_id=new_task.user_id,
            title=new_task.title,
            description=new_task.description,
            completed=new_task.completed,
            created_at=new_task.created_at,
            updated_at=new_task.updated_at
        ),
        "message": "Task created successfully"
    }


@router.get("/", response_model=dict)
async def list_tasks(
    completed: bool = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all tasks for the authenticated user

    Args:
        completed: Optional filter by completion status (true/false)
        current_user: Authenticated user from JWT token
        db: Database session

    Returns:
        List of user's tasks sorted by creation date (newest first)
    """
    # Query tasks filtered by user_id
    statement = select(Task).where(Task.user_id == current_user.id)

    # Apply completed filter if provided
    if completed is not None:
        statement = statement.where(Task.completed == completed)

    # Sort by created_at DESC
    statement = statement.order_by(Task.created_at.desc())

    tasks = db.exec(statement).all()

    return {
        "success": True,
        "data": [
            TaskResponse(
                id=task.id,
                user_id=task.user_id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
            for task in tasks
        ]
    }


@router.get("/{task_id}", response_model=dict)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific task by ID

    Args:
        task_id: Task ID to retrieve
        current_user: Authenticated user from JWT token
        db: Database session

    Returns:
        Task information

    Raises:
        HTTPException: 404 if task not found or 403 if unauthorized
    """
    # Query task by ID and user_id (security: prevent cross-user access)
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == current_user.id
    )
    task = db.exec(statement).first()

    if not task:
        # Check if task exists but belongs to different user
        statement_exists = select(Task).where(Task.id == task_id)
        task_exists = db.exec(statement_exists).first()

        if task_exists:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this task"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} not found"
            )

    return {
        "success": True,
        "data": TaskResponse(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
    }


@router.put("/{task_id}", response_model=dict)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a task's title and description

    Args:
        task_id: ID of the task to update
        task_data: Updated task data
        current_user: Authenticated user from JWT token
        db: Database session

    Returns:
        Updated task information

    Raises:
        HTTPException: 404 if task not found, 403 if not authorized, 400 if validation fails
    """
    # Find task with authorization check
    task = db.exec(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    ).first()

    if not task:
        # Check if task exists but belongs to another user
        task_exists = db.exec(select(Task).where(Task.id == task_id)).first()
        if task_exists:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this task"
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Validate title is not empty
    if not task_data.title or not task_data.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title cannot be empty"
        )

    # Validate title length
    if len(task_data.title) > 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title must be 200 characters or less"
        )

    # Validate description length if provided
    if task_data.description and len(task_data.description) > 2000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task description must be 2000 characters or less"
        )

    # Update task
    task.title = task_data.title.strip()
    task.description = task_data.description.strip() if task_data.description else None
    task.updated_at = datetime.utcnow()

    db.add(task)
    db.commit()
    db.refresh(task)

    return {
        "success": True,
        "data": TaskResponse(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at,
            updated_at=task.updated_at
        ),
        "message": "Task updated successfully"
    }


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a task

    Args:
        task_id: ID of the task to delete
        current_user: Authenticated user from JWT token
        db: Database session

    Raises:
        HTTPException: 404 if task not found, 403 if not authorized
    """
    # Find task with authorization check
    task = db.exec(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    ).first()

    if not task:
        # Check if task exists but belongs to another user
        task_exists = db.exec(select(Task).where(Task.id == task_id)).first()
        if task_exists:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this task"
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Delete task
    db.delete(task)
    db.commit()


@router.patch("/{task_id}/status", response_model=dict)
async def update_task_status(
    task_id: int,
    status_data: TaskStatusUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Toggle task completion status

    Args:
        task_id: ID of the task to update
        status_data: New completion status
        current_user: Authenticated user from JWT token
        db: Database session

    Returns:
        Updated task information

    Raises:
        HTTPException: 404 if task not found, 403 if not authorized
    """
    # Find task with authorization check
    task = db.exec(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    ).first()

    if not task:
        # Check if task exists but belongs to another user
        task_exists = db.exec(select(Task).where(Task.id == task_id)).first()
        if task_exists:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this task"
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update status
    task.completed = status_data.completed
    task.updated_at = datetime.utcnow()

    db.add(task)
    db.commit()
    db.refresh(task)

    return {
        "success": True,
        "data": TaskResponse(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at,
            updated_at=task.updated_at
        ),
        "message": "Task status updated successfully"
    }
