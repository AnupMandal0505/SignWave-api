import json
import numpy as np
from channels.generic.websocket import AsyncWebsocketConsumer
import pickle

class ASLConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        try:
            # Extract hand landmark data from request
            data = json.loads(text_data)
            print(data)

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

                await self.send(text_data=json.dumps({
                    'multiHandLandmarks': data['multiHandLandmarks'],
                    'resultData': predicted_character
                }))

            else:
                await self.send(text_data=json.dumps({
                'message': "No multiHandLandmarks"
            }))

        except Exception as e:
            await self.send(text_data=json.dumps({
                'error': str(e)
            }))

    def extract_landmark_features(self, landmarks):
        # Extract (x, y) and normalize as in the original `CallingAPI` class
        x_ = [landmark.x for landmark in landmarks]
        y_ = [landmark.y for landmark in landmarks]
        min_x, min_y = min(x_), min(y_)
        return [(landmark.x - min_x, landmark.y - min_y) for landmark in landmarks]
