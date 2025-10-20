import json
import logging
import os
import requests # Essential for making external API calls

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

# Configure basic logging to see issues in your Codespaces console
logger = logging.getLogger(__name__)

# --- 1. GEMINI API CONFIGURATION ---

# Retrieve the API Key from the environment. This key MUST be set 
# in your Codespaces .env file (as GEMINI_API_KEY).
API_KEY = os.environ.get("GEMINI_API_KEY") 

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent"

# System instruction to define the chatbot's persona and rules
SYSTEM_INSTRUCTION = (
    "You are a friendly, professional, and efficient Customer Support Assistant for an e-commerce "
    "company. Your name is 'Assist AI'. Respond concisely and clearly. "
    "Focus only on providing solutions or requesting necessary details for issues like "
    "shipping, refunds, and product information. DO NOT write long paragraphs."
)

# --- 2. GENERATIVE AI SERVICE LAYER ---

def get_ai_response_from_gemini(user_query):
    """
    Constructs the payload and sends the request to the Gemini API.
    """
    if not API_KEY:
        # Raise an exception if the key is missing from the environment
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    
    # Construct the API payload
    payload = {
        "contents": [{
            "parts": [{"text": user_query}]
        }],
        "systemInstruction": {
            "parts": [{"text": SYSTEM_INSTRUCTION}]
        },
        # Optional: set temperature for more focused (less creative) responses for support
        "config": { 
            "temperature": 0.2
        }
    }

    # The request URL includes the API Key as a query parameter
    url_with_key = f"{GEMINI_API_URL}?key={API_KEY}"
    
    try:
        # Make the API call
        response = requests.post(
            url_with_key,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(payload),
            timeout=15 # Set a timeout for the external request
        )
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        # Parse the response and extract the generated text
        result = response.json()
        
        # Accessing the generated text from the response structure
        generated_text = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
        
        if generated_text:
            return generated_text
        else:
            logger.error(f"Gemini API returned no text: {result}")
            return "I apologize, the AI service failed to generate a response."

    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP Request Error to Gemini API: {e}")
        return "I'm experiencing connectivity issues with my AI brain. Please try again shortly."
    except Exception as e:
        logger.error(f"Unexpected error in Gemini request: {e}")
        return "An internal error occurred while processing your query."


# --- 3. DJANGO API VIEW ---

@csrf_exempt
@api_view(['POST'])
def chat_api_view(request):
    """
    The main API endpoint that connects the frontend to the generative AI service.
    """
    try:
        data = json.loads(request.body)
        user_message = data.get('user_message', '').strip()
    except json.JSONDecodeError:
        logger.error("Invalid JSON received.")
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    
    if not user_message:
        return JsonResponse({'error': 'User message is empty'}, status=400)

    # Process message using the Generative AI Service
    try:
        ai_response = get_ai_response_from_gemini(user_message)
        
        return JsonResponse({'ai_response': ai_response})
    
    except ValueError as e:
        # This catches the error if the API key is missing
        logger.critical(f"Configuration Error: {e}")
        return JsonResponse({
            'ai_response': f"Configuration Error: {e}. Please ensure your GEMINI_API_KEY is set in your .env file."
        }, status=500)
    
    except Exception as e:
        logger.error(f"Error in chat_api_view: {e}")
        return JsonResponse({'ai_response': "A critical server error occurred."}, status=500)
