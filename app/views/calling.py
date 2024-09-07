from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pickle
import numpy as np

class CallingAPI(APIView):
    def post(self, request):
        try:
            # Extract hand landmark data from request
            data = request.data.get('calldata')
            # print(data)

            # Load the pre-trained model
            with open('./model1.p', 'rb') as file:
                model_dict = pickle.load(file)
            model = model_dict['model']

            # Define the labels for the gestures (classes used in your training)
            labels_dict = [
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                'del', 'nothing', 'space'
            ]

            # Get the number of features the model expects (42 features for one hand)
            n_features = model.n_features_in_
            print(f"Model expects {n_features} features.")

            data_aux = []
            x_ = []
            y_ = []

            # Check if the incoming data contains hand landmarks
            if data['multiHandLandmarks']:
                for hand_landmarks in data['multiHandLandmarks']:
                    for i in range(len(hand_landmarks)):
                        # Get x and y coordinates for each landmark
                        x = hand_landmarks[i]['x']
                        y = hand_landmarks[i]['y']

                        x_.append(x)
                        y_.append(y)

                    # Normalize x and y coordinates by subtracting the minimum values
                    for i in range(len(hand_landmarks)):
                        x = hand_landmarks[i]['x']
                        y = hand_landmarks[i]['y']
                        data_aux.append(x - min(x_))
                        data_aux.append(y - min(y_))

                # Check if the number of features is correct
                if len(data_aux) != n_features:
                    print(f"Feature mismatch: expected {n_features}, got {len(data_aux)}")
                    raise Exception(f"Feature mismatch: expected {n_features}, got {len(data_aux)}")

                # Make a prediction using the model
                prediction = model.predict([np.asarray(data_aux)])
                predicted_character = prediction[0]  # Get the predicted label

                return JsonResponse({
                    'Response': predicted_character
                })

            else:
                # If no hand landmarks are provided, return an error
                return JsonResponse({
                    'status': 400,
                    'error': 'No hand landmarks detected.',
                    'message': 'Please provide valid hand landmark data.',
                    'data': {}
                }, status=400)

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
