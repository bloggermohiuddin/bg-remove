import base64
import io
import requests
from flask import Flask, request, jsonify
from rembg import remove
from PIL import Image

app = Flask(__name__)

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    # Ensure the request contains the image URL
    if 'image_url' not in request.json:
        return jsonify({'success': False, 'message': 'No image URL provided'}), 400
    
    try:
        # Get the image URL from the request
        image_url = request.json['image_url']
        
        # Fetch the image from the URL
        response = requests.get(image_url)
        if response.status_code != 200:
            return jsonify({'success': False, 'message': 'Failed to fetch the image from the URL'}), 400
        
        # Open the image using PIL
        image = Image.open(io.BytesIO(response.content))
        
        # Remove the background
        output_image = remove(image)
        
        # Convert the processed image to PNG and then to base64
        buffered = io.BytesIO()
        output_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        # Return the base64 image in the JSON response
        return jsonify({'success': True, 'image': img_str})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
