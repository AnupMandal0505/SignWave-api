import whisper
from django.http import JsonResponse
from pydub import AudioSegment
from io import BytesIO
import tempfile
import os
from rest_framework.views import APIView
from rest_framework.response import Response

class AudioToTextAPI(APIView):
    def post(self, request):
        print(7888)
        try:
            
            audio_file = request.FILES['audio_file']
            print(audio_file)
            # Convert the InMemoryUploadedFile to a BytesIO object
            audio_bytes = BytesIO(audio_file.read())

            # Convert the audio file to WAV format using pydub
            audio_segment = AudioSegment.from_file(audio_bytes)
            wav_io = BytesIO()
            audio_segment.export(wav_io, format='wav')
            wav_io.seek(0)  # Move the pointer to the beginning of the BytesIO object

            # Create a temporary file to save the WAV data
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav_file:
                temp_wav_file.write(wav_io.getvalue())
                temp_wav_file.close()  # Close the file to ensure it is saved

                # Load the Whisper model
                model = whisper.load_model("base")

                # Load audio using Whisper's load_audio method (from the temporary file)
                audio = whisper.load_audio(temp_wav_file.name)
                audio = whisper.pad_or_trim(audio)

                # Make log-Mel spectrogram and move to the same device as the model
                mel = whisper.log_mel_spectrogram(audio).to(model.device)

                # Detect the spoken language
                _, probs = model.detect_language(mel)
                detected_language = max(probs, key=probs.get)
                print(f"Detected language: {detected_language}")

                # Decode the audio
                options = whisper.DecodingOptions(fp16=False)
                result = whisper.decode(model, mel, options)
                print(result.text)

                # Clean up the temporary file
                os.remove(temp_wav_file.name)

                # Return JSON response
                return JsonResponse({
                    'detected_language': detected_language,
                    'transcribed_text': result.text
                })
            
        except Exception as e:
            print(e)
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'Not get data',
                'data': {}
            }
            return Response(error_response, status=400)