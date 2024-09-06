from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import google.generativeai as genai
import os


# Configure the API key once, outside the class
api_key = os.getenv('GENAI_API_KEY')
genai.configure(api_key=api_key)

class ChatbotAPI(APIView):
    def post(self, request):
        try:
            # Extract the prompt (question) from the request data
            prompt = request.data.get('question')

            # If no question provided, return a bad request response
            if not prompt:
                return Response({'error': 'Question not provided'}, status=status.HTTP_400_BAD_REQUEST)

            # Initialize the generative model
            model = genai.GenerativeModel("gemini-pro")

            # Generate a response from the model
            response = model.generate_content(prompt)
            print(1)

            # Build the chat history (if you want to maintain chat context)
            chat_history = [{
                "user": prompt,
                "bot": response.text
            }]

            # Return the AI-generated response
            return Response({
                'chat_history': chat_history  # Optional: Return chat history for reference
            })

        except Exception as e:
            # Log the exception for debugging
            print(e)

            # Return error response
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': str(e),  # Include the exception message for better error tracking
                'data': {}
            }
            return Response(error_response, status=400)
