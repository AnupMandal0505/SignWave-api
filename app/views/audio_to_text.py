from google.cloud import speech
from google.oauth2 import service_account
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import os
import tempfile

class AudioToTextAPI(APIView):
    def post(self, request):
        try:
            # Get the uploaded audio file
            audio_file = request.FILES['audio_file']

            # Save the audio file to a temporary location
            # with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as temp_file:
            #     temp_file.write(audio_file.read())
            #     temp_file_path = temp_file.name

            # Load the service account credentials from the JSON file
            credentials = service_account.Credentials.from_service_account_file(
                'google-cred.json'
            )

            # Initialize the Google Cloud Speech client with the credentials
            client = speech.SpeechClient(credentials=credentials)

            # Load audio content into memory
            # with open(temp_file_path, "rb") as f:
            #     audio_content = f.read()

            # Prepare Google Cloud speech recognition request
            audio = speech.RecognitionAudio(content=audio_file.read())
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
                language_code="en-US",
                enable_automatic_punctuation=True
            )

            # Transcribe the audio file
            response = client.recognize(config=config, audio=audio)

            # Extract transcribed text
            transcribed_text = ""
            for result in response.results:
                transcribed_text += result.alternatives[0].transcript

            # Return the transcribed text
            return JsonResponse({
                'transcribed_text': transcribed_text
            })

        except Exception as e:
            print(f"Error: {e}")
            return Response({
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'Error during transcription',
                'data': {}
            }, status=400)
