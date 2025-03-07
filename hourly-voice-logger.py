import os
import time
import datetime
import sounddevice as sd
import wave
import schedule
from plyer import notification

def record_audio(duration=30, filename=None):
    """Records audio for the given duration (default: 30 seconds) and saves it as a WAV file."""
    if filename is None:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"recordings/{timestamp}.wav"
    
    if not os.path.exists("recordings"):
        os.makedirs("recordings")
    
    samplerate = 44100  # Standard sample rate
    channels = 1  # Mono audio
    
    print("Recording... Speak now!")
    notification.notify(
        title="Time to Log Your Progress!",
        message="Recording for the next 30 seconds...",
        timeout=5
    )
    
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels, dtype='int16')
    sd.wait()
    
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(audio_data.tobytes())
    
    print(f"Recording saved: {filename}")
    notification.notify(
        title="Recording Saved!",
        message=f"Your voice log has been saved as {filename}",
        timeout=5
    )

def hourly_prompt():
    """Triggers the recording process every hour."""
    print("Prompting for voice log...")
    notification.notify(
        title="Hourly Check-In",
        message="Time to reflect on your past hour! Click to start recording.",
        timeout=10
    )
    time.sleep(5)
    record_audio()

# Schedule the hourly reminder
schedule.every().hour.at(":00").do(hourly_prompt)

print("Hourly Voice Logger is running...")
while True:
    schedule.run_pending()
    time.sleep(1)
