"""
Flask API for serving the ML model
"""
from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np

app = Flask(__name__)

# Load the trained model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Load model info (feature names and target names)
with open('model_info.pkl', 'rb') as f:
    model_info = pickle.load(f)

@app.route('/')
def home():
    """Render home page with form"""
    return render_template('index.html', 
                         feature_names=model_info['feature_names'],
                         target_names=model_info['target_names'])

@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint for making predictions
    Expects JSON with features:
    {
        "features": [sepal_length, sepal_width, petal_length, petal_width]
    }
    """
    try:
        data = request.get_json()
        features = data['features']
        
        # Validate input
        if len(features) != 4:
            return jsonify({
                'error': 'Expected 4 features: sepal length, sepal width, petal length, petal width'
            }), 400
        
        # Make prediction
        features_array = np.array(features).reshape(1, -1)
        prediction = model.predict(features_array)[0]
        probability = model.predict_proba(features_array)[0]
        
        # Get class name
        class_name = model_info['target_names'][prediction]
        
        # Prepare response
        response = {
            'prediction': int(prediction),
            'class_name': class_name,
            'probabilities': {
                model_info['target_names'][i]: float(prob)
                for i, prob in enumerate(probability)
            }
        }
        
        return jsonify(response)
    
    except KeyError:
        return jsonify({'error': 'Missing "features" key in request'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'model': 'loaded'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
