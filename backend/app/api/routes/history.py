from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)

from sqlalchemy.orm import Session


from ...database import get_app_db

from ...auth.jwt_handler import get_current_user

from ...models.user import User

from ...schemas.history import (
    HistoryCreate,
    HistoryResponse,
    HistoryListResponse,
)

from ...services.history_service import (
    history_service,
)



router = APIRouter(
    prefix="/api/history",
    tags=["Query History"],
)



@router.post(
    "",
    response_model=HistoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_history(
    data: HistoryCreate,
    db: Session = Depends(get_app_db),
    current_user: User = Depends(get_current_user),
):
    """
    Save query execution history.
    """


    try:

        return history_service.create_history(
            db=db,
            user_id=current_user.id,
            data=data,
        )


    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Failed to save query history",
        )




@router.get(
    "",
    response_model=HistoryListResponse,
)
def get_history(
    page: int = Query(
        1,
        ge=1,
    ),

    page_size: int = Query(
        20,
        ge=1,
        le=100,
    ),

    status_filter: str | None = Query(
        None,
        alias="status",
    ),

    connection_id: int | None = Query(
        None,
    ),

    db: Session = Depends(get_app_db),

    current_user: User = Depends(get_current_user),
):
    """
    Get user query history.
    """


    try:

        items = history_service.get_history(
            db=db,
            user_id=current_user.id,
            page=page,
            page_size=page_size,
            status=status_filter,
            connection_id=connection_id,
        )


        return HistoryListResponse(
            items=items,
            page=page,
            page_size=page_size,
            total=len(items),
        )


    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve history",
        )




@router.get(
    "/{history_id}",
    response_model=HistoryResponse,
)
def get_history_by_id(
    history_id: int,

    db: Session = Depends(get_app_db),

    current_user: User = Depends(get_current_user),
):
    """
    Get single history record.
    """


    history = history_service.get_history_by_id(
        db=db,
        user_id=current_user.id,
        history_id=history_id,
    )


    if history is None:

        raise HTTPException(
            status_code=404,
            detail="History record not found",
        )


    return history




@router.delete(
    "/{history_id}",
)
def delete_history(
    history_id: int,

    db: Session = Depends(get_app_db),

    current_user: User = Depends(get_current_user),
):
    """
    Delete one history record.
    """


    deleted = history_service.delete_history(
        db=db,
        user_id=current_user.id,
        history_id=history_id,
    )


    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="History record not found",
        )


    return {
        "message":
        "History deleted successfully"
    }




@router.delete(
    "",
)
def clear_history(
    db: Session = Depends(get_app_db),

    current_user: User = Depends(get_current_user),
):
    """
    Delete all user history.
    """


    deleted_count = history_service.clear_history(
        db=db,
        user_id=current_user.id,
    )


    return {
        "message":
        "History cleared successfully",

        "deleted_count":
        deleted_count,
    }