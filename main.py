from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import SessionLocal, engine  
from util.contact_tables import Contact , Base
from schemas.schemas import ContactRequest, ContactResponse 
from util.crud import find_existing_contacts, create_contact, update_contact_to_secondary
from util.get_db import get_db  


app = FastAPI()


Base.metadata.create_all(bind=engine)


get_db()

@app.post("/identify", response_model=ContactResponse)
def identify_contact(request: ContactRequest, db: Session = Depends(get_db)):
    if not request.email and not request.phoneNumber:
        raise HTTPException(status_code=400, detail="At least one of email or phoneNumber is required.")

    existing_contacts = find_existing_contacts(db, request.email, request.phoneNumber)

    if not existing_contacts:
        
        new_contact = create_contact(db, request.email, request.phoneNumber, None, "primary")
        return ContactResponse(
            primaryContactId=new_contact.id,
            emails=[new_contact.email] if new_contact.email else [],
            phoneNumbers=[new_contact.phoneNumber] if new_contact.phoneNumber else [],
            secondaryContactIds=[]
        )

    
    primary_contact = min(existing_contacts, key=lambda c: c.createdAt)
    primary_id = primary_contact.id

    
    if request.email and request.email not in [c.email for c in existing_contacts if c.email]:
        new_secondary = create_contact(db, request.email, request.phoneNumber, primary_id, "secondary")
        existing_contacts.append(new_secondary)
    
    if request.phoneNumber and request.phoneNumber not in [c.phoneNumber for c in existing_contacts if c.phoneNumber]:
        new_secondary = create_contact(db, request.email, request.phoneNumber, primary_id, "secondary")
        existing_contacts.append(new_secondary)

    for contact in existing_contacts:
        if contact.linkPrecedence == "primary" and contact.id != primary_id:
            update_contact_to_secondary(db, contact, primary_id)

    
    emails = list({c.email for c in existing_contacts if c.email})
    phoneNumbers = list({c.phoneNumber for c in existing_contacts if c.phoneNumber})
    secondaryContactIds = [c.id for c in existing_contacts if c.linkPrecedence == "secondary"]

    return ContactResponse(
        primaryContactId=primary_id,
        emails=emails,
        phoneNumbers=phoneNumbers,
        secondaryContactIds=secondaryContactIds
    )
