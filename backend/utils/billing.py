from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import stripe
from datetime import datetime, timedelta

from api import models
from database import get_db
from config import STRIPE_SECRET_KEY

router = APIRouter()
stripe.api_key = STRIPE_SECRET_KEY

# Create Stripe customer and subscription
@router.post("/create-subscription")
def create_subscription(partner_id: int, plan_id: int, db: Session = Depends(get_db)):
    partner = db.query(models.Partner).filter(models.Partner.id == partner_id).first()
    plan = db.query(models.BillingPlan).filter(models.BillingPlan.id == plan_id).first()

    if not partner or not plan:
        raise HTTPException(status_code=404, detail="Partner or Plan not found")

    # Create Stripe Customer
    customer = stripe.Customer.create(
        email=partner.contact_email,
        name=partner.name
    )

    # Create Stripe Subscription
    subscription = stripe.Subscription.create(
        customer=customer.id,
        items=[{"price_data": {
            "currency": plan.currency,
            "product_data": {"name": plan.name},
            "unit_amount": int(plan.price * 100),
            "recurring": {"interval": plan.interval}
        }}],
        expand=["latest_invoice.payment_intent"]
    )

    new_subscription = models.Subscription(
        partner_id=partner_id,
        plan_id=plan_id,
        stripe_customer_id=customer.id,
        stripe_subscription_id=subscription.id,
        status="active",
        started_at=datetime.utcnow(),
        ends_at=datetime.utcnow() + timedelta(days=30)
    )
    db.add(new_subscription)
    db.commit()

    return {
        "message": "Subscription created successfully",
        "stripe_subscription_id": subscription.id
    }


# Cancel subscription
@router.post("/cancel-subscription")
def cancel_subscription(subscription_id: int, db: Session = Depends(get_db)):
    subscription = db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()

    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")

    stripe.Subscription.delete(subscription.stripe_subscription_id)

    subscription.status = "canceled"
    db.commit()

    return {"message": "Subscription canceled successfully"}


# Verify subscription status
@router.get("/check-subscription/{partner_id}")
def check_subscription(partner_id: int, db: Session = Depends(get_db)):
    subscription = db.query(models.Subscription).filter(models.Subscription.partner_id == partner_id).first()

    if not subscription or subscription.status != "active":
        raise HTTPException(status_code=404, detail="No active subscription found")

    return {
        "status": subscription.status,
        "ends_at": subscription.ends_at
    }
