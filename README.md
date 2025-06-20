# DeskBot – Personal Voice Assistant

A Python-powered desktop assistant with **real-time speech recognition** and **natural language responses**. Control applications, automate tasks, and get intelligent answers — all through voice commands.

---

## How It Works

- Listens to your **voice commands** via microphone
- Uses **Google Speech Recognition** to convert speech to text
- If a casual query:
  - Responds using **OpenAI**
  - Speaks the response aloud with `pyttsx3`
  - Saves the reply in a `.txt` file
- If a **system/task command**:
  - Opens websites or apps
  - Tells the current time
- Option to reset chat history or quit the assistant anytime

---

## Tech Stack

| Component      | Technology                         |
|----------------|-------------------------------------|
| Language       | Python                              |
| Voice Input    | SpeechRecognition, PyAudio          |
| Voice Output   | pyttsx3                             |
| Intelligence   | OpenAI API      |
| Tasks & Apps   | OS, Webbrowser, Platform Modules    |
| Interface      | Command-line (Terminal-based)       |

---

## Features

- Real-time speech recognition from mic input
- Intelligent chat powered by OpenAI
- Text-to-speech voice replies
- Opens YouTube, Google, Wikipedia, and more
- Announces system time
- Saves OpenAI responses in `Openai/` folder
- "Reset chat" to clear context
- Exit/quit anytime

---

## Example Commands

| You Say                                | DeskBot Does                           |
|----------------------------------------|----------------------------------------|
| "Open YouTube"                         | Launches YouTube in default browser    |
| "What is the time?"                    | Tells current system time              |
| "Using artificial intelligence, explain gravity" | Responds via OpenAI and saves it     |
| "Reset chat"                           | Clears conversation memory             |
| "Quit" or "Exit"                       | Stops the assistant                    |
