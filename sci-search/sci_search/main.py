from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .database import SessionLocal, Base, engine
from .models import Document, Page, Field
from . import schemas

from .dao.document_dao import DocumentDAO
Base.metadata.create_all(engine)

app = FastAPI()
document_dao = DocumentDAO()


def get_db_return():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/docs/", response_model=schemas.Document)
def create_doc(doc: schemas.DocumentBase, db: Session = Depends(get_db)):
    return document_dao.create_doc(db, doc)

@app.get("/docs/", response_model=List[schemas.Document])
def read_docs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return document_dao.get_docs(db, skip, limit)

@app.get("/docs/{doc_id}", response_model=schemas.Document)
def read_doc(doc_id: int, db: Session = Depends(get_db)):
    return document_dao.get_doc_from_id(db, doc_id)



# def simple_main():
#     db = get_db_return()
#     db.add(Document(title = "First document", pages = [Page(page_number = 1, content = "First page content"), Page(page_number = 2, content = "Second Page")], fields = [Field(name = "name", value = "value")]))
#     db.commit()


# if __name__ == "__main__":
#     simple_main()

