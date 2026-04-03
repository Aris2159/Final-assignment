# **Binary Search Guessing Game With Gradio**

## About
An interactive web app where the computer guesses the number you pick from an array using Binary Search. It only works with numbers from 1-100.

**Python Version 3.11+**
___
### You can:
    - Use a random sorted array of 10 numbers
    - Type your own array comma-separated
    - Guide the computer with Higher. Lower, or Correct
    - See guess history and number of steps
___
### Features:
    - Binary Search logic
    - Gradio interface
    - Custom or random array input
    - Step-by-step game history
    - Reset/start controls
___
### Project Files
- ```app.py```: Gradio UI and App logic
- ```requirements.txt```: All the Python dependencies needed
___
### How it Works
    1. The app picks the middle number in the sorted array.
    2. You tell the app if your number is Higher, Lower, or Correct.
    3. The search range shrinks each step.
    4. The app stops when it finds your number or the range is empty.
**Binary Search time complexity is O(log n)**
___
### Installation
1. Create and activate a virtual environment.
2. Install dependencies:
`pip install -r requirements.txt`

- If needed, install gradio directly:
    - `pip install --upgrade gradio`
___
### Run
- python `app.py`
- Gradio will open a local app in your browser
___
## Usage
1. Start the game using:
    - Start (uses current/typed array), or
    - Generate New Array
2. Think of one number from the shown array.
3. Click:
    - `Higher` if your number is bigger than the guess
    - `Lower` if your number is smaller than the guess
    - `Correct` when the guess matches
4. Check the History panel for all actions.

### Video on How To Use
