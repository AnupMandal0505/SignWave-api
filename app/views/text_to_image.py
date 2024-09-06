# # my_ml_app/views.py
# import pickle
# from django.shortcuts import render
# from django.http import JsonResponse

# # Load the model
# with open('my_ml_app/ml_model/model.pkl', 'rb') as model_file:
#     model = pickle.load(model_file)

# def predict(request):
#     if request.method == 'POST':
#         data = request.POST['data']  # Get input data from the request
#         prediction = model.predict([data])  # Use the model to make a prediction
#         return JsonResponse({'prediction': prediction.tolist()})

#     return render(request, 'predict.html')
