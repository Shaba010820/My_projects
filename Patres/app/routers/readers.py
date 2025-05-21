from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.readers import Reader
from app.routers.auth import get_current_user
from app.schemas.readers import ReaderCreate, ReaderRead, ReaderUpdate

router = APIRouter(prefix="/readers", tags=["readers"])


@router.post("/", response_model=ReaderRead)
def create_reader(
    reader: ReaderCreate, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    existing_reader = db.query(Reader).filter(Reader.email == reader.email).first()
    if existing_reader:
        raise HTTPException(
            status_code=400, detail="Reader with this email already exists"
        )

    db_reader = Reader(**reader.model_dump())
    db.add(db_reader)
    db.commit()
    db.refresh(db_reader)
    return db_reader


@router.get("/", response_model=list[ReaderRead])
def list_readers(db: Session = Depends(get_db), user=Depends(get_current_user)):
    readers = db.query(Reader).all()
    return readers


@router.get("/{reader_id}", response_model=ReaderRead)
def get_reader(
    reader_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    return reader


@router.put("/{reader_id}", response_model=ReaderRead)
def update_reader(
    reader_id: int,
    reader_update: ReaderUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")

    for field, value in reader_update.model_dump(exclude_unset=True).items():
        setattr(reader, field, value)

    db.commit()
    db.refresh(reader)
    return reader


@router.delete("/{reader_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reader(
    reader_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")

    db.delete(reader)
    db.commit()
    return None
