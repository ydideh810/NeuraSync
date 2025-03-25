from fastapi import Request, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from api.models import License

async def verify_license_middleware(request: Request, call_next):
    db: Session = next(get_db())

    license_key = request.headers.get("X-License-Key")

    if not license_key:
        raise HTTPException(status_code=401, detail="Missing license key")

    license = db.query(License).filter(License.license_key == license_key).first()

    if not license or license.status != "active":
        raise HTTPException(status_code=403, detail="Invalid or expired license")

    response = await call_next(request)
    return response
