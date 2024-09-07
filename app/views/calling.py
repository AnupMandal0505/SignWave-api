from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pickle
# import mediapipe as mp
import numpy as np


class CallingAPI(APIView):
    def post(self, request):
        try:
            data = request.data.get('calldata')

                        
            with open('./model.p', 'rb') as file:
                model_dict = pickle.load(file)
            model = model_dict['model']



            # Define the labels for the gestures (all your classes)
            labels_dict = [
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                'del', 'nothing', 'space'
            ]

            # Get the number of features the model expects
            n_features = model.n_features_in_
            print(f"Model expects {n_features} features.")

            data_aux = []
            x_ = []
            y_ = []

            if data.multiHandLandmarks:
                for hand_landmarks in data.multiHandLandmarks:
                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y

                        x_.append(x)
                        y_.append(y)

                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y
                        data_aux.append(x - min(x_))
                        data_aux.append(y - min(y_))
                # Check if the number of features is correct
            if len(data_aux) != n_features:
                print(f"Feature mismatch: expected {n_features}, got {len(data_aux)}")
                raise Exception(f"Feature mismatch: expected {n_features}, got {len(data_aux)}")
        
            # Make a prediction based on the model
            prediction = model.predict([np.asarray(data_aux)])
            predicted_character = prediction[0]  # Directly use the string prediction

            return JsonResponse({
                                'Response': predicted_character
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



