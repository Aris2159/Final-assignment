#This program will let user input an array or generate a random array with 10 elements then ask user to select a number and program will find the number in the
#array using binary search by asking user if the number is higher or lower then x number and go lower or higher until the number is found or not found in 
# the array. The program will also count the number of guesses it takes to find the number. It will also ask user to play again after the game is over.
# The program fronend is in gradio and the backend is in python. 

# Import all the libraries for the program. Gradio for the frontend and random for generating values for the array.
import gradio as gr
import random as r

def start():
    arr = sorted([r.randint(1, 100) for _ in range(10)])
    return init_state_from_array(arr)

def init_state_from_array(arr):
    low = 0
    high = len(arr) - 1
    guessCount = 1

    mid = (low + high) // 2
    guess = arr[mid]

    message = f"Is your number {guess}?"
    return arr, low, high, guessCount, guess, message, mid

def parse_array_text(arr_text):
    parts = [p.strip() for p in arr_text.split(",") if p.strip()]
    if not parts:
        raise ValueError("Please enter at least one integer.")
    numbers = [int(p) for p in parts]
    return sorted(numbers)

def guess_number(arr, low, high, guessCount, guess, message, user_input, mid):
    if user_input == "Higher":
        low = mid + 1
    elif user_input == "Lower":
        high = mid - 1
    elif user_input == "Correct":
        return arr, low, high, guessCount, guess, f"Congratulations! You've found the number {guess} in {guessCount} guesses.", mid
    

    
    guessCount += 1
    if low > high:
        return arr, low, high, guessCount, guess, "Number not found in the array.", mid
    mid = (low + high) // 2
    guess = arr[mid]
    message = f"Is your number {guess}?"
    return arr, low, high, guessCount, guess, message, mid

def use_typed_array(arr_text, current_arr):
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

def generate_random_array():
    arr, low, high, guessCount, guess, message, mid = start()
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
