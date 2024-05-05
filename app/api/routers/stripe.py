import stripe
from fastapi import APIRouter, Request, HTTPException

from app.core.config import StripeConfig
from app.api.controllers.stripe import process_stripe_event


endpoint_secret = StripeConfig.STRIPE_WEBHOOK_SECRET

router = APIRouter()


@router.post("/webhook")
async def stripe_webhook(request: Request):
    event = None
    payload = await request.body()
    sig_header = request.headers["stripe-signature"]

    if not sig_header:
        raise HTTPException(status_code=400, detail="Missing Stripe signature header.")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Invalid payload received.{e}")
    except stripe.error.SignatureVerificationError as e:
        raise HTTPException(status_code=500, detail=f"Invalid Stripe signature.{e}")

    return await process_stripe_event(event)
