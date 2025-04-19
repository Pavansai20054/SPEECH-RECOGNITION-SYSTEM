import speech_recognition as sr
import time
import os

def recognize_speech_from_mic(recognizer, microphone):
    """
    Transcribe speech from recorded from an audio file.

    Args:
        recognizer (sr.Recognizer): The SpeechRecognition Recognizer instance.
        microphone (sr.Microphone): The SpeechRecognition Microphone instance.

    Returns:
        dict: A dictionary containing the transcription, success status, and error message.
    """
    # adjust the recognizer settings for ambient noise
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=5)
        print("Say something!")
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }
    
    try:
        # Using Google Web Speech API for recognition
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["success"] = False
        response["error"] = "Unable to recognize speech"

    return response

if __name__ == "__main__":
    # create recognizer and microphone instances
    r = sr.Recognizer()
    mic = sr.Microphone()

    # Define the output Markdown file
    output_file = "transcription.md"

    print(f"Speak now... Say 'close this conversation' to stop.")

    # Loop to continuously listen for speech
    while True:
        speech_input = recognize_speech_from_mic(r, mic)

        if speech_input["success"]:
            transcription = speech_input["transcription"]
            print(f"Recognized: {transcription}")

            # Check if the stop phrase is in the transcription (case-insensitive)
            if "close this conversation" in transcription.lower():
                print("Stop phrase detected. Ending conversation.")
                break # Exit the while loop

            # Append the recognized text to the Markdown file if not the stop phrase
            with open(output_file, "a") as f:
                f.write(f"- {transcription}\n") 
            print(f"Saved to {output_file}")

        elif speech_input["error"] == "API unavailable":
            print("Could not request results from speech recognition service; {0}".format(speech_input["error"]))
        elif speech_input["error"] == "Unable to recognize speech":
            print("Could not understand audio")

        # Add a small delay to avoid continuous high CPU usage
        time.sleep(0.5)

    # Final message after exiting the loop
    print("Transcription complete. Check the Markdown file for results.")