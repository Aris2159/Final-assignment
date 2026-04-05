# **Binary Search Guessing Game With Gradio**

## About
An interactive web app where the computer guesses the number you pick from an array using Binary Search. It only works with numbers from 1-100. 
It can only only do 10 element at max. A lot of error handling has been put to this so the app would not break.

**Python Version 3.11+**
___
### You can:
    - Use a random sorted array of 10 numbers
    - Type your own array comma-separated
    - Guide the computer with Higher, Lower, or Correct
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
___
## Video on How To Use

[[Watch the demo video](assets/demo.mp4)](https://github.com/Aris2159/Final-assignment/blob/main/assets/demo.mp4)

___

## Problem Breakdown and Computational Thinking
- **Decomposition:**
1. Get an array
2. Sort the array so Binary Search can work correctly
3. Set search boundaries
4. Find the middle value
5. Based on user response:
    - Higher -> move low to mid + 1
    - Lower -> move high to mid - 1
    - Correct -> stop and show the result
6. Repeat until the number is found or the range is empty
7. Record each step in history and show total guesses

- **Pattern Recognition:**

The same comparison pattern repeats each round:

    - Compare the guess with the user's target feedback
    - Remove half of the remaining search space
    - Recalculate the middle
    - Ask again

- **Abstraction:** 

The user does not need to see internal details like index math at every step.

The interface simplifies this into three actions:
``` 
- Higher
- Lower
- Correct
```
The complexity is hidden, and interaction stays simple.


- **Algorithm Design:**

    - **Input:** User provides an array and feedback.
    - **Processing:** Sort array compute middle, update boundaries using Binary Search rules, count guesses, and store history.
    - **Output:** Display current guess question, success/faliure message, guess count, and full action history.

___
### **Flow Chart:**
```
Start
  |
Get array (typed/random) → Sort
  |
Set low=0, high=n-1
  |
Guess middle value
  |
User feedback?
  |- Higher → low = mid + 1
  |- Lower  → high = mid - 1
  |- Correct → Found (show guesses)
  |
If low > high -> Not found
Else repeat
```
___
## Hugging Face Link
https://huggingface.co/spaces/Ariss2159/CISC_121
___
## Author & Acknowledgment
**Author:** Aris

**Acknowledgment:**
- Inspired by binary search algorithms
- AI has been **used** for helping make the UI for gradio but not in logic. It has also been **used** in debugging the program as there was an error that was not being found. All the code has been wrrite on my own with some help of AI to help me deepen my understanding and UI is made with help of AI. (AI used for this is Github Copilot)
- Built using Gradio framework
