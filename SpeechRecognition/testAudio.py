import speech_recognition as sr

def write_to_text(stream):
    with open('output.txt', 'a') as file:
        file.write(stream + '\n')

'''
RUN ONLY IN COLAB 

from google.colab import drive
from google.colab import files

# Mount Google Drive to Colab
drive.mount('/content/gdrive')

# Define the local file path
local_file_path = 'path/to/your/local/file.txt'

# Define the destination folder and file name on Google Drive
drive_folder = '/content/gdrive/My Drive/'
drive_file_name = 'uploaded_file.txt'

# Copy the local file to Google Drive
!cp "{local_file_path}" "{drive_folder}{drive_file_name}"
'''

def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something:")
        recognizer.adjust_for_ambient_noise(source)

        try:
            while True:
                audio = recognizer.listen(source, timeout=None)
                stream = recognizer.recognize_google(audio)

                if stream:  
                    print("You said: " + stream)
                    write_to_text(stream)

        except sr.UnknownValueError:
            print("Google Web Speech API could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Web Speech API; {0}".format(e))
        except KeyboardInterrupt:
            print("Recognition interrupted by user")

if __name__ == "__main__":
    recognize_speech()
