
[click me](#installation) to skip to installation && usage!

---

# Speeding up TorToiSe inference 5x

This is a working project to drastically boost the performance of TorToiSe, without modifying the base models. **Expect speedups of _5~10x_**, and hopefully 20x or larger when this project is complete.

This repo adds the following config options for TorToiSe for faster inference:

- [x] (`--kv_cache`) enabling of [KV cache](https://kipp.ly/blog/transformer-inference-arithmetic/#kv-cache) for MUCH faster GPT sampling
- [x] (`--half`) half precision inference where possible
- [x] (`--sampler dpm++2m`) [DPM-Solver](https://github.com/LuChengTHU/dpm-solver) samplers for better diffusion
- [x] (disable with `--low_vram`) option to toggle cpu offloading, for high vram users


## Current results

All results listed were generated with a slightly undervolted RTX 3090 on Ubuntu 22.04, with the following base command:

```sh
./script/tortoise-tts.py --voice emma --seed 42 --text "$TEXT"
```


Half precision currently significantly worsens outputs, so I do not recommend enabling it unless you are happy with the samples linked. Using `cond_free` with half precision seems to produce decent outputs.

## Installation

### AMD INSTALLATION IS NOT SUPPORTED, please don't try it

There are two methods for installation.


### Docker install

```shell
docker build buildx -t transcription-server .
```

### Run directly
```sh
cd server
```
```sh
uvicorn api:app --reload --host localhost --port 8000
```



### Local Installation

If you want to use this on your own computer, you must have an NVIDIA GPU.

First, install pytorch using these instructions: [https://pytorch.org/get-started/locally/](https://pytorch.org/get-started/locally/).
On Windows, I **highly** recommend using the Conda installation path. I have been told that if you do not do this, you
will spend a lot of time chasing dependency problems.

Next, install TorToiSe and it's dependencies:

```shell
git clone https://github.com/neonbjb/tortoise-tts.git
cd tortoise-tts
python -m pip install -r ./requirements.txt
python setup.py install
```

### API

Tortoise can be used programmatically, like so:

```python
reference_clips = [utils.audio.load_audio(p, 22050) for p in clips_paths]
tts = api.TextToSpeech()
pcm_audio = tts.tts_with_preset("your text here", voice_samples=reference_clips, preset='fast')
```

Here is an example API call:

```python
import requests

# URL of the FastAPI app
url = "http://localhost:8000/generate/"

# Parameters structured as a dictionary
data = {
    "text": "Good morning, thank you for joining me here today. How are you doing?.",
    "voice": "geralt",
    "preset": "very_fast" #[fast, very_fast, ultra_fast]
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

```


### Available perameter

Voices:

```python
TODO
```

Presets:

```python
TODO
```
Configurations:

```python
TODO
```