# %%
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import subprocess
import os
import asyncio

script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the Python script
ffmpeg_connect_script = os.path.join(script_dir, 'ffmpeg-connect.sh')
join_room_script = os.path.join(script_dir, 'join-room-script.sh')
create_room_script = os.path.join(script_dir, 'create-room.sh')

# %%
nltk.download('punkt')
nltk.download('stopwords')
running_processes = []

# %%
training_data = [
    ("Can I join the meeting room?", "joining"),
    ("Is there any available room?", "joining"),
    ("Can I be part of this room?", "joining"),
    ("I want to leave the conference room.", "leaving"),
    ("Leaving the room now.", "leaving"),
    ("I'm done with this meeting room.", "leaving"),
    ("Create a new chat room.", "creating"),
    ("Can you help me create a room?", "creating"),
    ("Let's create a private room for our team.", "creating"),

]

# %%
def preprocess_text(text):
    tokens = word_tokenize(text.lower())

    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token not in stop_words]

    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in filtered_tokens]

    return stemmed_tokens

def extract_features(text):
    return {word: True for word in preprocess_text(text)}

training_set = [(extract_features(text), intent) for text, intent in training_data]
classifier = nltk.NaiveBayesClassifier.train(training_set)


# %%
def predict_intent(text):
    features = extract_features(text)
    return classifier.classify(features)

# %%
async def run_ffmpeg_command(room_name, video_sock, audio_sock):
    command = [ffmpeg_connect_script, video_sock, audio_sock]
    try:
        process = await asyncio.create_subprocess_exec(*command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        running_processes.append(process)
        print(f"{room_name} - Video and audio connected.")
    except subprocess.CalledProcessError as e:
        print(f"Error connecting video and audio for {room_name}: {e.stderr.decode('utf-8')}")

async def join_room_script(room_name, video_sock, audio_sock):
    command = ['./join-room-script.sh', room_name, video_sock, audio_sock]
    try:
        process = await asyncio.create_subprocess_exec(*command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        running_processes.append(process)
        print(f"{room_name} - Joined the room.")
    except subprocess.CalledProcessError as e:
        print(f"Error joining the room {room_name}: {e.stderr.decode('utf-8')}")

async def create_room_script(room_name):
    command = ['./create-room.sh',room_name]
    try:
        process = await asyncio.create_subprocess_exec(*command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        running_processes.append(process)
        print(f"{room_name} - Room Created")
    except subprocess.CalledProcessError as e:
        print(f"{room_name} - Error joining the room")

async def handle_joining():
    await run_ffmpeg_command("The View", "/tmp/myvideo.sock", "/tmp/myaudio.sock")
    await join_room_script("The View", "/tmp/myvideo.sock", "/tmp/myaudio.sock")
    print("Joined!!")

async def handle_creating():
    print(os.getcwd())
    await create_room_script("The View")
    print("Creating...")

async def handle_leaving():
    for process in running_processes:
        process.kill()
        await process.wait()
    running_processes.clear()
    print("Leaving...")

def invoke_command(predicted_intent):
    if predicted_intent == "joining":
        asyncio.run(handle_joining())
    elif predicted_intent == "creating":
        asyncio.run(handle_creating())
    elif predicted_intent == "leaving":
        asyncio.run(handle_leaving())
    else:
        print("I do not understand!")


# %%

user_input = input("Enter prompt: ")
predicted_intent = predict_intent(user_input)
print("Predicted Intent:", predicted_intent)
#asyncio.run(invoke_command(predicted_intent))
invoke_command(predicted_intent)

# %%
running_processes


