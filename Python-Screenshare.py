from flask import Flask, jsonify
from PIL import ImageGrab
import numpy as np
# Download packages (It's easy search yourself)

app = Flask(__name__)

# Store the last frame colors to compare for changes
last_colors = None

def capture_screen():
    global last_colors

    # Capture the screen and resize to match the number of parts
    screenshot = ImageGrab.grab()
    screenshot = screenshot.resize((0, 0)) # Resize to your resolution (Length, Height) (Change it to your cols and rows)
    screenshot = np.array(screenshot)
    colors = screenshot.reshape(-1, 3).tolist()

    if last_colors is None:                                                                      
        last_colors = colors                                                                      
        changes = list(range(len(colors)))  # First frame, send all colors                        
    else:                                                                                                                           
        changes = [i for i, c in enumerate(colors) if c != last_colors[i]]                                                                        
        last_colors = colors  # Update the cached frame                                                                                                                                                             
                                                                                                                        
    # Return only changed parts and their indices                                                                               
    return {"changes": changes, "colors": [colors[i] for i in changes]}                           
                                                                                                 
@app.route('/screen', methods=['GET'])                                                                                                  
def serve_screenshot():                                                                                                         
    color_data = capture_screen()                                                                                                       
    return jsonify(color_data)                                                                                                                                                                                                       

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=0) # Replace with the port number you want to use
