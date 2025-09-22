# AI Reel Studio

AI Reel Studio is a web-based application that allows users to create short video reels from images and text. The application uses AI to generate a voiceover from the user-provided text and combines it with the uploaded images to create a video file.

## Features

* **Web-based interface:** Simple and intuitive web interface for creating reels.
* **Image uploads:** Users can upload multiple images to be included in the reel.
* **Text-to-speech:** AI-powered text-to-speech functionality to create a voiceover for the reel.
* **Automatic reel generation:** The application automatically combines the images and audio to generate a reel.
* **Gallery:** A gallery to view all the generated reels.

## How it Works

1.  The user uploads images and provides text for the voiceover on the "Create Reel" page.
2.  The application saves the uploaded images and text to a unique folder for that user.
3.  A background process continuously monitors for new user uploads.
4.  When a new upload is detected, the process:
    1.  Converts the provided text to an audio file using a text-to-speech API.
    2.  Uses FFmpeg to create a video slideshow from the uploaded images.
    3.  Combines the video and audio to create the final reel.
5.  The generated reel is then available in the "Gallery".

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/ggauravky/my-all-python-projects-.git](https://github.com/ggauravky/my-all-python-projects-.git)
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd "My-all-Python-Projects--a6fb79425309d7ed3044b8e477c683c286bbf003/AI Reel-Studio"
    ```
3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up your ElevenLabs API key:**
    * Create a `config.py` file.
    * Add your ElevenLabs API key to the file as follows:
        ```python
        ELEVENLABS_API_KEY = "YOUR_API_KEY"
        ```
5.  **Run the main application:**
    ```bash
    python main.py
    ```
6.  **Run the reel generation process in a separate terminal:**
    ```bash
    python generate_process.py
    ```
7.  Open your web browser and go to `http://127.0.0.1:5000` to use the application.

## Technologies Used

* **Python:** The core programming language used for the application.
* **Flask:** A web framework for Python used to build the web interface.
* **FFmpeg:** A command-line tool for handling video and audio files.
* **ElevenLabs API:** Used for the text-to-speech functionality.

## File Descriptions

* **`main.py`**: The main Flask application file. It handles the web server and user requests.
* **`generate_process.py`**: A script that runs in the background to process user uploads and generate reels.
* **`text_to_audio.py`**: A module that uses the ElevenLabs API to convert text to speech.
* **`config.py`**: A configuration file to store the ElevenLabs API key.
* **`templates/`**: A directory containing the HTML templates for the web interface.
* **`static/`**: A directory containing the static files (CSS, images, etc.) for the web interface.
* **`user_uploads/`**: A directory where user-uploaded files are stored.
* **`done.txt`**: A file that keeps track of the folders that have already been processed.
* **`ffmpeg_command.txt`**: A sample FFmpeg command for creating a reel.