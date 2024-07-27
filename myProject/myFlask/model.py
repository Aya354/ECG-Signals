import joblib  # For loading serialized models (replace if needed)


def load_model(model_path):
    """Loads the pre-trained model."""
    return joblib.load(model_path)

def predict_class(model, data):
    """Makes predictions on the data using the loaded model."""
    prediction = model.predict(data)  # Replace with your model's prediction method
    return prediction.tolist()

def interpret_prediction(label):
    if label == 0 :
        result = "Congratulations, this patient doesn't have Arrhythmia condition."
    elif label == 1:
        result = "Unfortunately, this patient has SVEB (Supra-ventricular Ectopic Beat) Arrhythmia condition."
    elif label == 2:
        result = "Unfortunately, this patient has VEB (Ventricular Ectopic Beat) Arrhythmia condition."
    else:
        results = "Unfortunately, this patient has F (Fusion Beat) Arrhythmia condition."
    return result
