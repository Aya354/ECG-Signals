from django.shortcuts import render, redirect
#from flask import Flask, request, jsonify
#from flask_cors import CORS  # Consider using CORS if necessary
#import requests  # For making requests to Flask app
from .model import load_model, predict_class, interpret_prediction
import pandas as pd
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response


def predict_view(request):
    if request.method == "POST":
        # Get data from the form (adjust based on your form)
        file = request.FILES.get('file') 

        # Read the file into a DataFrame
        data = pd.read_excel(file)

        for col in data.columns:
            data[col] = pd.to_numeric(data[col], errors='coerce')


        # Load the model (optional, can be done outside the view)
        model = load_model("C:/Users/hp/Desktop/Project/myProject/myFlask/model_pipeline.joblib")

        # Make prediction
        predictions = predict_class(model, data)

        # Optionally interpret predictions
        interpreted_predictions = []
        for pred in predictions:
            interpreted_predictions.append(interpret_prediction(pred))

        return render(request, "myFlask/prediction_result.html", {"predictions": interpreted_predictions})
    return render(request, "myFlask/upload_data.html")


@api_view(['POST'])
def predict_api(request):
    if request.method == "POST":
        try:
            # Get data from the request (assuming it's in an Excel file)
            file = request.FILES.get('file')  # Adjust based on your form input name
            
            # Read the file into a Pandas DataFrame
            data = pd.read_excel(file)

            # Clean the data (if necessary)
            for col in data.columns:
                data[col] = pd.to_numeric(data[col], errors='coerce')

            # Load the machine learning model
            model_path = "C:/Users/hp/Desktop/Project/myProject/myFlask/model_pipeline.joblib"
            model = load_model(model_path)

            # Make predictions using the model
            predictions = predict_class(model, data)

            # Interpret predictions (if needed)
            interpreted_predictions = []
            for pred in predictions:
                interpreted_predictions.append(interpret_prediction(pred))

            # Return predictions as JSON response
            return JsonResponse({"predictions": interpreted_predictions})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)

