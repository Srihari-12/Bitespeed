from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from util.contact_tables import Contact 

from typing import List, Optional

def find_existing_contacts(db: Session, email: Optional[str], phoneNumber: Optional[str]) -> List[Contact]:
    
    contacts = db.query(Contact).filter(
        (Contact.email == email) | (Contact.phoneNumber == phoneNumber)
    ).all()

    if len(contacts) > 1:
        
        primary_contact = min(contacts, key=lambda c: c.createdAt)
        for contact in contacts:
            if contact.id != primary_contact.id and contact.linkPrecedence == "primary":
                contact.linkPrecedence = "secondary"
                contact.linkedId = primary_contact.id
                db.commit()
                db.refresh(contact)

    return contacts

def create_contact(db: Session, email: Optional[str], phoneNumber: Optional[str], linkedId: Optional[int], linkPrecedence: str):
   
    new_contact = Contact(
        email=email,
        phoneNumber=phoneNumber,
        linkedId=linkedId,
        linkPrecedence=linkPrecedence
    )
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact

def update_contact_to_secondary(db: Session, contact: Contact, new_primary_id: int):
    
    contact.linkPrecedence = "secondary"
    contact.linkedId = new_primary_id
    db.commit()
    db.refresh(contact)
