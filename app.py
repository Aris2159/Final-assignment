# Import all the libraries for the program. Gradio for the frontend and random for generating values for the array.
import gradio as gr
import random as r

# Define a function to start the game. It Generates a random sorted array of 10 integers between 1 and 100.
def start():
    arr = sorted([r.randint(1, 100) for _ in range(10)])
    # Return the initial state of the game, including the array
    return init_state_from_array(arr)

# Define a function for initializing state from the array. It sets the low and high, guess count, mid and guess values based on the input array, and message to ask the user if there number is the guess.
def init_state_from_array(arr):
    # Define the variables need to keep track of the game state
    # define low and high to keep track of the current search range
    low = 0
    high = len(arr) - 1
    # Guess count to keep how many guesses the program has made and starts at 1 if its 0 then its a logical error because 
    # we are making the first guess right after this function is called
    guessCount = 1

    # To find the mid you add low and high and divide by 2 this will give the index of the middle element in the current range of the array
    mid = (low + high) // 2
    # The guess is the value at the mid index of the array
    guess = arr[mid]

    # The message is a f string that is asking user if this is their number and it will display the guess value in the message
    message = f"Is your number {guess}?"
    # Return all the variables to use later in the game
    return arr, low, high, guessCount, guess, message, mid

# Define a function to parse the array text input by the user.
def parse_array_text(arr_text):
    # Split the input text by commas, strip whitespace, and convert to integers. It also filters out any empty parts that may result from extra commas or spaces. 
    # If there are no valid integers, it raises a ValueError.
    parts = [p.strip() for p in arr_text.split(",") if p.strip()]
    #If there are no valid integers, it raises a ValueError.
    if not parts:
        # This is to make sure that the user enters atleast one integer in the input
        # If it doesn't it will raise an error and prompt the user to enter a valid input
        raise ValueError("Please enter at least one integer.")
    # Convert the valid parts to integers and store them in a list. This will be the array that the game will use for guessing
    # Store the integers in a list called numbers.
    numbers = [int(p) for p in parts]
    # This will return the sorted list of integers that the user entered. 
    # This is important to sort for binary search to work correctly
    return sorted(numbers)

# Define a function to handle the user response to guesses. This function takes in the current game state and the user input and updates the game state
# It is also calling variables from other functions to update the game state based on the user input of whether the guess is higher or lower or correct
def guess_number(arr, low, high, guessCount, guess, message, mid, user_input):
    # Define a if statment  and see if its equal to higher?
    if user_input == "Higher":
        # If its higher then we add low to mid + 1 because we know that the number must be higher 
        # than the current guess so we can eliminate all the numbers that are less than or equal to the current guess and update low to mid + 1
        low = mid + 1
    # If the user input is lower then
    elif user_input == "Lower":
        # we update the high to mid - 1 because we know that the number must be lower than the current guess
        high = mid - 1
    # If the user input is correct then we return with a congratulatory message and the number of guesses it took to find the number
    elif user_input == "Correct":
        return arr, low, high, guessCount, guess, f"Congratulations! You've found the number {guess} in {guessCount} guesses.", mid
    

    
    guessCount += 1
    if low > high:
        return arr, low, high, guessCount, guess, "Number not found in the array.", mid
    mid = (low + high) // 2
    guess = arr[mid]
    message = f"Is your number {guess}?"
    return arr, low, high, guessCount, guess, message, mid

# Define a function to handle the user input using a costume array.
# This function takes in the text input for the array and the current array state
def use_typed_array(arr_text, current_arr):
    # raw_text is the stripped version of the input text. If the input is empty or only contains white space, then
    raw_text = (arr_text or "").strip()
    if not raw_text:
        low = 0
        high = len(current_arr) - 1
        guessCount = 0
        mid = (low + high) // 2
        guess = current_arr[mid]
        message = "Please type integers separated by commas, e.g. 3, 10, 2, 8"
        return current_arr, low, high, guessCount, guess, message, mid, str(current_arr), message

    try:
        arr = parse_array_text(raw_text)
    except ValueError:
        low = 0
        high = len(current_arr) - 1
        guessCount = 0
        mid = (low + high) // 2
        guess = current_arr[mid]
        message = "Invalid input. Use integers separated by commas, e.g. 3, 10, 2, 8"
        return current_arr, low, high, guessCount, guess, message, mid, str(current_arr), message

    arr, low, high, guessCount, guess, message, mid = init_state_from_array(arr)
    return arr, low, high, guessCount, guess, message, mid, str(arr), message

# Define a function to generate a new random array and start the game with it.
# This function is only called when the user clicks the "Generate New Array" button and it will creata new random array
def generate_random_array():
    # All the variables init_state_from_array, guess_number, use_typed_array are called to generate a new random array and start the game with it.
    # they are being sent to the start function to generate a new random
    arr, low, high, guessCount, guess, message, mid = start()
    # This will return the new game state with new random array and the message to ask the user if this is their number
    return arr, low, high, guessCount, guess, message, mid, str(arr), message

def start_game(arr_text, current_arr):
    if (arr_text or "").strip():
        return use_typed_array(arr_text, current_arr)
    return generate_random_array()

def on_higher(arr, low, high, guessCount, guess, message, mid):
    arr, low, high, guessCount, guess, message, mid = guess_number(
        arr, low, high, guessCount, guess, message, "Higher", mid
    )
    return arr, low, high, guessCount, guess, message, mid, str(arr), message

def on_lower(arr, low, high, guessCount, guess, message, mid):
    arr, low, high, guessCount, guess, message, mid = guess_number(
        arr, low, high, guessCount, guess, message, "Lower", mid
    )
    return arr, low, high, guessCount, guess, message, mid, str(arr), message

def on_complete(arr, low, high, guessCount, guess, message, mid):
    arr, low, high, guessCount, guess, message, mid = guess_number(
        arr, low, high, guessCount, guess, message, "Correct", mid
    )
    return arr, low, high, guessCount, guess, message, mid, str(arr), message

#All the history of what player did
def append_history(history, action, message):
    line = f"{action}: {message}"
    if history:
        return f"{history}\n{line}"
    return line

def reset_history(action, message):
    return f"{action}: {message}"

def start_game_click(arr_text, current_arr, history):
    arr, low, high, guessCount, guess, message, mid, arr_text_out, message_out = start_game(arr_text, current_arr)
    history_out = reset_history("Start", message_out)
    return arr, low, high, guessCount, guess, message, mid, arr_text_out, message_out, history_out, history_out

def use_typed_array_click(arr_text, current_arr, history):
    arr, low, high, guessCount, guess, message, mid, arr_text_out, message_out = use_typed_array(arr_text, current_arr)
    history_out = reset_history("Use Typed Array", message_out)
    return arr, low, high, guessCount, guess, message, mid, arr_text_out, message_out, history_out, history_out

def generate_random_array_click(history):
    arr, low, high, guessCount, guess, message, mid, arr_text_out, message_out = generate_random_array()
    history_out = reset_history("Generate New Array", message_out)
    return arr, low, high, guessCount, guess, message, mid, arr_text_out, message_out, history_out, history_out

def on_higher_click(arr, low, high, guessCount, guess, message, mid, history):
    arr, low, high, guessCount, guess, message, mid, arr_text_out, message_out = on_higher(
        arr, low, high, guessCount, guess, message, mid
    )
    history_out = append_history(history, "Higher", message_out)
    return arr, low, high, guessCount, guess, message, mid, arr_text_out, message_out, history_out, history_out

def on_lower_click(arr, low, high, guessCount, guess, message, mid, history):
    arr, low, high, guessCount, guess, message, mid, arr_text_out, message_out = on_lower(
        arr, low, high, guessCount, guess, message, mid
    )
    history_out = append_history(history, "Lower", message_out)
    return arr, low, high, guessCount, guess, message, mid, arr_text_out, message_out, history_out, history_out

def on_complete_click(arr, low, high, guessCount, guess, message, mid, history):
    arr, low, high, guessCount, guess, message, mid, arr_text_out, message_out = on_complete(
        arr, low, high, guessCount, guess, message, mid
    )
    history_out = append_history(history, "Correct", message_out)
    return arr, low, high, guessCount, guess, message, mid, arr_text_out, message_out, history_out, history_out

with gr.Blocks() as demo:
    initial_arr, initial_low, initial_high, initial_guess_count, initial_guess, initial_message, initial_mid = start()
    initial_history = f"Init: {initial_message}"

    arr = gr.State(initial_arr)
    low = gr.State(initial_low)
    high = gr.State(initial_high)
    guessCount = gr.State(initial_guess_count)
    guess = gr.State(initial_guess)
    message = gr.State(initial_message)
    mid = gr.State(initial_mid)
    history = gr.State(initial_history)
    
    gr.Markdown("### Binary Search Game")
    gr.Markdown("Think of a number in the array and I will try to guess it. After each guess, tell me if your number is Higher or Lower than my guess.")
    
    with gr.Row(equal_height=True):
        arr_display = gr.Textbox(
            value=str(initial_arr),
            label="Array (comma-separated integers)",
            interactive=True,
            lines=2,
            scale=1,
        )
        message_display = gr.Textbox(
            value=initial_message,
            label="Result",
            interactive=False,
            lines=2,
            scale=1,
        )

    history_display = gr.Textbox(
        value=initial_history,
        label="History",
        interactive=False,
        lines=10,
    )
    
    with gr.Row():
        higher_button = gr.Button("Higher")
        lower_button = gr.Button("Lower")
        complete_button = gr.Button("Correct")


    higher_button.click(
        on_higher_click,
        inputs=[arr, low, high, guessCount, guess, message, mid, history],
        outputs=[arr, low, high, guessCount, guess, message, mid, arr_display, message_display, history, history_display],
    )

    with gr.Row():
        start_button = gr.Button("Start")
        use_typed_button = gr.Button("Use Typed Array")
        generate_button = gr.Button("Generate New Array")

    start_button.click(
        start_game_click,
        inputs=[arr_display, arr, history],
        outputs=[arr, low, high, guessCount, guess, message, mid, arr_display, message_display, history, history_display],
    )

    use_typed_button.click(
        use_typed_array_click,
        inputs=[arr_display, arr, history],
        outputs=[arr, low, high, guessCount, guess, message, mid, arr_display, message_display, history, history_display],
    )

    generate_button.click(
        generate_random_array_click,
        inputs=[history],
        outputs=[arr, low, high, guessCount, guess, message, mid, arr_display, message_display, history, history_display],
    )


    complete_button.click(
        on_complete_click,
        inputs=[arr, low, high, guessCount, guess, message, mid, history],
        outputs=[arr, low, high, guessCount, guess, message, mid, arr_display, message_display, history, history_display],
    )

    
    lower_button.click(
        on_lower_click,
        inputs=[arr, low, high, guessCount, guess, message, mid, history],
        outputs=[arr, low, high, guessCount, guess, message, mid, arr_display, message_display, history, history_display],
    )


demo.launch(share=True) # Launch the Gradio app and share it with a public link
