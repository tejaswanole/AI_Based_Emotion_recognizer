from flask import Flask, render_template, jsonify
import subprocess # Allows us to run other python scripts
import os

app = Flask(__name__)

# 1. Route for the Homepage
@app.route('/')
def home():
    return render_template('index.html')

# 2. API to Run Project 1 (Mood DJ)
@app.route('/run_mood_dj', methods=['POST'])
def run_mood_dj():
    try:
        # This command runs your other script
        # verify the filename matches EXACTLY what you have on disk
        subprocess.Popen(['python', 'main_spotify_dj.py'], shell=True)
        return jsonify({"status": "success", "message": "Mood DJ Started!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# 3. API to Run Project 2 (Focus Guardian)
@app.route('/run_focus_guardian', methods=['POST'])
def run_focus_guardian():
    try:
        subprocess.Popen(['python', 'focus_guardian_final.py'], shell=True)
        return jsonify({"status": "success", "message": "Focus Guardian Started!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    print("✅ Server Running! Go to http://127.0.0.1:5000 in your browser")
    app.run(debug=True)