import speech_recognition as sr
import pyttsx3
import pygame
import pygame.camera
import os
import google.generativeai as genai
import PIL


pygame.camera.init()
# Detect available cameras
camlist = pygame.camera.list_cameras()

# Initialize the speech recognition engine
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()


def check_image_exists(filename="captured_image.jpg"):
    return os.path.exists(filename)

def delete_image(filename="captured_image.jpg"):
    try:
        os.remove(filename)
        print(f"Image '{filename}' has been deleted successfully.")
    except FileNotFoundError:
        print(f"Image '{filename}' does not exist in the current directory.")


def recognize_speech():
    try:
        with sr.Microphone() as source:
            print("Listening for 'hello'...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)

            # Recognize speech
            recognized_text = recognizer.recognize_google(audio)
            print(f"Recognized: {recognized_text}")
            return recognized_text.lower()
    except sr.WaitTimeoutError:
        print("Timeout: No speech detected.")
        return None
    except sr.UnknownValueError:
        print("Error: Could not understand audio.")
        return None

def say_hello():
    if camlist:
        # Initialize and start the camera
        cam = pygame.camera.Camera(camlist[0], (1920, 1080))
        cam.start()

        # Capture a single image
        image = cam.get_image()

        # Save the image
        pygame.image.save(image, "captured_image.jpg")
    else:
        print("No camera detected on the current device.")


def vision_ai(arument = None):
    os.environ['GOOGLE_API_KEY'] = "YOUR API KEY"
    genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

    image = PIL.Image.open('.\captured_image.jpg')
    vision_model = genai.GenerativeModel('gemini-pro-vision')
    text_model=genai.GenerativeModel('gemini-pro')

    if check_image_exists():
        response = vision_model.generate_content([f":{arument}",image])
    
    
    response_text=response.text

    if check_image_exists():
        delete_image()


    print(response_text)
    return response_text

def text_ai(arument = None):
    os.environ['GOOGLE_API_KEY'] = "AIzaSyCUQJoNEnB-mInBtRnf3ooOhLOUUQMx9d0"
    genai.configure(api_key = os.environ['GOOGLE_API_KEY'])


    text_model=genai.GenerativeModel('gemini-pro')

    
    response = text_model.generate_content(f"{arument}")
   
    response_text=response.text

    print(response_text)
    return response_text


def text_to_speech(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set properties (optional)
    engine.setProperty("rate", 150)  # Speed of speech (words per minute)
    engine.setProperty("volume", 1.0)  # Volume (0.0 to 1.0)

    # Convert text to speech
    engine.say(text)

    # Save the speech as an audio file (optional)
    engine.save_to_file(text, "output.mp3")

    # Run the engine
    engine.runAndWait()

vision_list=["what is this","use camera","can u detect","what is there"]
speachtext=""
print(speachtext)

def main():
    while True:
        recognized_text = recognize_speech()
        speachtext=recognized_text

        if recognized_text:
            if any(char in recognized_text for char in vision_list):
                say_hello()
                
                input_text = vision_ai(recognized_text)
                text_to_speech(input_text)
                print(f"Text converted to speech: {input_text}")
            
            else:
                input_text = text_ai(recognized_text)
                text_to_speech(input_text)
                print(f"Text converted to speech: {input_text}")

if __name__ == "__main__":
    main()
