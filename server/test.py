import requests


def transcribe_audio(file_path, save_path=None):
    url = 'http://3.96.135.101:8080/transcribe'
    files = {'file': (file_path, open(file_path, 'rb'), 'audio/mpeg')}
    data = {'save_path': save_path} if save_path else {}

    response = requests.post(url, files=files, data=data)
    return response.json()


if __name__ == "__main__":
    file_path = '/home/ajeema/code/transcribe-server/server/AFH19911011.ogg'
    save_path = None # set None if not needed

    transcription_response = transcribe_audio(file_path, save_path)
    for line in transcription_response["transcription"]:
        print(line)
