from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.models import Animal
from app.utils.paginator import Pagination, PaginationResult

router = APIRouter()


@router.get("/animals", response_model=PaginationResult[schemas.AnimalDetail], tags=["Animal"])
def list_animals(p: Pagination = Depends(Pagination), db: Session = Depends(get_db)):
    queryset = db.query(Animal)
    return p.apply(queryset, schemas.AnimalDetail)
