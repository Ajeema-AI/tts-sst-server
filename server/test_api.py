import requests

# URL of the FastAPI app
url = "http://localhost:8000/generate/"

# Parameters structured as a dictionary
data = {
    "text": "Good morning, thank you for joining me here today. How are you doing?.",
    "voice": "geralt",
    "preset": "ultra_fast"
}

# Send POST request with JSON body
response = requests.post(url, json=data)  # Note the use of `json=data`

# Check if the request was successful
if response.status_code == 200:
    # Save the generated audio file
    with open('generated_speech.wav', 'wb') as f:
        f.write(response.content)
    print("Audio file generated and saved as 'generated_speech.wav'.")
else:
    print("Failed to generate speech:", response.json())
