from PyPDF2 import PdfReader
from tkinter.filedialog import askopenfilename
from gtts import gTTS
import pyttsx3

# Select the PDF file
book = askopenfilename()
pdfreader = PdfReader(book)
pages = len(pdfreader.pages)

# Extract text from all pages
full_text = ""
for num in range(pages):
    page = pdfreader.pages[num]
    text = page.extract_text()
    if text:
        full_text += text

# Check if any text was extracted
if not full_text.strip():
    print("❌ No readable text found in the PDF.")
    exit()

# Ask user whether to speak or save as MP3
print("\nWhat would you like to do?")
print("1. Speak the content")
print("2. Save as MP3 file")
choice = input("Enter 1 or 2: ")

if choice == "1":
    # Speak using pyttsx3
    print("🔊 Speaking the PDF content...")
    player = pyttsx3.init()
    player.say(full_text)
    player.runAndWait()

elif choice == "2":
    # Save as MP3 using gTTS
    print("💾 Saving as audiobook.mp3...")
    tts = gTTS(text=full_text, lang='en')
    tts.save("audiobook.mp3")
    print("✅ Saved as 'audiobook.mp3' successfully.")

else:
    print("⚠️ Invalid choice. Please enter 1 or 2.")
