from flask import Flask, request, jsonify
from flask_cors import CORS
from aa_dd_model import AADDModel

app = Flask(__name__)
# Configure CORS to accept requests from GitHub Pages and localhost
CORS(app, origins=[
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://localhost',
    'https://*.github.io'  # Allow all GitHub Pages domains
])

# Create a single instance of the model
model = AADDModel()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

@app.route('/calculate', methods=['POST'])
def calculate():
    """Calculate new economic state"""
    try:
        state = request.json
        if not state:
            return jsonify({'error': 'No state data provided'}), 400
        
        result = model.calculate_economic_state(state)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-curves', methods=['POST'])
def generate_curves():
    """Generate AA and DD curves"""
    try:
        state = request.json
        if not state:
            return jsonify({'error': 'No state data provided'}), 400
            
        aa_curve = model.generate_aa_curve(state)
        dd_curve = model.generate_dd_curve(state)
        return jsonify({
            'aa_curve': aa_curve,
            'dd_curve': dd_curve
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/reset', methods=['POST'])
def reset():
    """Reset the model"""
    try:
        model.reset()
        return jsonify({
            'gdp': model.gdp,
            'exchange_rate': model.exchange_rate,
            'current_account': model.current_account
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/calculate-gdp', methods=['POST'])
def calculate_gdp():
    """Calculate GDP change based on current state"""
    try:
        state = request.json
        if not state:
            return jsonify({'error': 'No state data provided'}), 400
            
        gdp_change = model.calculate_gdp_change(state)
        return jsonify({'gdp_change': gdp_change})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000) 