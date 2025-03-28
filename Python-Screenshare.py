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
    screenshot = screenshot.resize((256, 144)) # Resize to your resolution (Length, Height)
    screenshot = np.array(screenshot)
    colors = screenshot.reshape(-1, 3).tolist()

    # 𝐃𝐎𝐍'𝐓 𝐓𝐎𝐔𝐂𝐇 𝐀𝐍𝐘 𝐎𝐅 𝐓𝐇𝐈𝐒 𝐔𝐍𝐋𝐄𝐒𝐒 𝐘𝐎𝐔 𝐊𝐍𝐎𝐖 𝐖𝐇𝐀𝐓 𝐘𝐎𝐔'𝐑𝐄 𝐃𝐎𝐈𝐍𝐆 𝐘𝐎𝐔 𝐏𝐑𝐎𝐁𝐀𝐁𝐋𝐘 𝐃𝐎𝐍'𝐓
    if last_colors is None:                                                                      # 
        last_colors = colors                                                                     # 
        changes = list(range(len(colors)))  # First frame, send all colors                       # 
    else:                                                                                        #                                   
        changes = [i for i, c in enumerate(colors) if c != last_colors[i]]                       #                                                 
        last_colors = colors  # Update the cached frame                                          #                                                                                                                   
                                                                                                 #                       
    # Return only changed parts and their indices                                                #                               
    return {"changes": changes, "colors": [colors[i] for i in changes]}                          # 
                                                                                                 #
@app.route('/screen', methods=['GET'])                                                           #                                       
def serve_screenshot():                                                                          #                               
    color_data = capture_screen()                                                                #                                       
    return jsonify(color_data)                                                                   #                                   
    # 𝐘𝐎𝐔 𝐌𝐀𝐘 𝐍𝐎𝐖 𝐂𝐇𝐀𝐍𝐆𝐄 𝐂𝐎𝐃𝐄                                                                                                        

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80) # Replace with the port number you want to use