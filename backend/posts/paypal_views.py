"""
PayPal server-side integration views
Handles order creation, capture, and webhook events
"""
import os
import json
import hmac
import hashlib
from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import requests
from requests.auth import HTTPBasicAuth


# PayPal API configuration
PAYPAL_CLIENT_ID = os.environ.get('VITE_PAYPAL_CLIENT_ID', '')
PAYPAL_CLIENT_SECRET = os.environ.get('PAYPAL_CLIENT_SECRET', '')
PAYPAL_MODE = os.environ.get('PAYPAL_MODE', 'sandbox')  # 'sandbox' or 'live'

if PAYPAL_MODE == 'sandbox':
    PAYPAL_API_BASE = 'https://api-m.sandbox.paypal.com'
else:
    PAYPAL_API_BASE = 'https://api-m.paypal.com'


def get_paypal_access_token():
    """
    Get OAuth2 access token from PayPal
    """
    auth = HTTPBasicAuth(PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials'
    }
    
    response = requests.post(
        f'{PAYPAL_API_BASE}/v1/oauth2/token',
        auth=auth,
        headers=headers,
        data=data
    )
    
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise Exception(f'Failed to get PayPal access token: {response.text}')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_paypal_order(request):
    """
    Create a PayPal order (server-side)
    Expected payload:
    {
        "amount": "5.00",
        "currency": "EUR",
        "payee_email": "author@example.com",
        "description": "Donation for post"
    }
    """
    try:
        amount = request.data.get('amount')
        currency = request.data.get('currency', 'EUR')
        payee_email = request.data.get('payee_email')
        description = request.data.get('description', 'Donacija - Skriptomat')
        
        # Validation
        if not amount or not payee_email:
            return Response(
                {'error': 'Amount and payee_email are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        amount_decimal = Decimal(amount)
        if amount_decimal < Decimal('1.00'):
            return Response(
                {'error': 'Minimum donation amount is €1.00'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get PayPal access token
        access_token = get_paypal_access_token()
        
        # Create order
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        
        order_data = {
            'intent': 'CAPTURE',
            'purchase_units': [{
                'amount': {
                    'currency_code': currency,
                    'value': f'{amount_decimal:.2f}'
                },
                'description': description,
                'payee': {
                    'email_address': payee_email
                }
            }]
        }
        
        response = requests.post(
            f'{PAYPAL_API_BASE}/v2/checkout/orders',
            headers=headers,
            json=order_data
        )
        
        if response.status_code == 201:
            order = response.json()
            # Debug: log full order response to see what PayPal returns
            print("PayPal Order Response:", order)
            return Response({
                'orderID': order['id'],
                'status': order['status']
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {'error': 'Failed to create PayPal order', 'details': response.text},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def capture_paypal_order(request):
    """
    Capture a PayPal order after user approval (server-side)
    Expected payload:
    {
        "orderID": "5O190127TN364715T"
    }
    """
    try:
        order_id = request.data.get('orderID')
        
        if not order_id:
            return Response(
                {'error': 'orderID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get PayPal access token
        access_token = get_paypal_access_token()
        
        # Capture order
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        
        response = requests.post(
            f'{PAYPAL_API_BASE}/v2/checkout/orders/{order_id}/capture',
            headers=headers
        )
        
        if response.status_code == 201:
            capture_data = response.json()
            return Response({
                'status': capture_data['status'],
                'id': capture_data['id'],
                'capture_id': capture_data['purchase_units'][0]['payments']['captures'][0]['id']
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Failed to capture PayPal order', 'details': response.text},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@csrf_exempt
@require_http_methods(["POST"])
def paypal_webhook(request):
    """
    PayPal webhook endpoint to receive payment notifications
    This endpoint should be registered in PayPal Developer Dashboard
    
    Events to listen for:
    - PAYMENT.CAPTURE.COMPLETED
    - PAYMENT.CAPTURE.DENIED
    - PAYMENT.CAPTURE.REFUNDED
    """
    try:
        # Get webhook payload
        payload = json.loads(request.body.decode('utf-8'))
        event_type = payload.get('event_type')
        
        # Log the webhook event (in production, save to database)
        print(f'PayPal Webhook Event: {event_type}')
        print(f'Payload: {json.dumps(payload, indent=2)}')
        
        # Handle different event types
        if event_type == 'PAYMENT.CAPTURE.COMPLETED':
            # Payment was successfully captured
            capture_id = payload['resource']['id']
            amount = payload['resource']['amount']['value']
            currency = payload['resource']['amount']['currency_code']
            
            # TODO: Save transaction to database
            # Transaction.objects.create(
            #     capture_id=capture_id,
            #     amount=amount,
            #     currency=currency,
            #     status='completed'
            # )
            
            print(f'Payment completed: {capture_id} - {currency} {amount}')
        
        elif event_type == 'PAYMENT.CAPTURE.DENIED':
            # Payment was denied
            print('Payment denied')
        
        elif event_type == 'PAYMENT.CAPTURE.REFUNDED':
            # Payment was refunded
            refund_id = payload['resource']['id']
            print(f'Payment refunded: {refund_id}')
        
        # Always return 200 to acknowledge webhook receipt
        return JsonResponse({'status': 'success'}, status=200)
    
    except Exception as e:
        print(f'Webhook error: {str(e)}')
        return JsonResponse({'error': str(e)}, status=500)
