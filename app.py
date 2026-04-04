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
def guess_number(arr, low, high, guessCount, guess, message, user_input, mid):
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
        # This returns the current game state along with a congratulatory message that includes the number and the guess count
        return arr, low, high, guessCount, guess, f"Congratulations! You've found the number {guess} in {guessCount} guesses.", mid
    

    # Guess cound will add 1 to keep track of how many time the program made a guess. This will be important for the user to know how many guesses it took to find the number
    guessCount += 1
    # Uses is statment to check if the low is greater then high which will return with
    if low > high:
        # This will return with a message that the number is not found in the array and also the current game state.
        return arr, low, high, guessCount, guess, "Number not found in the array.", mid

    # If the game is still running then we calculate the new mid and guess based on the updated low and high values.
    # This will allow the program to make a new guess based on the user input and continue the game until the number is found.
    mid = (low + high) // 2
    # This will update the guess to have a new value in the array based on the new mid index
    guess = arr[mid]
    # This will update the message to ask the user if this is their number based on the new guessed value
    message = f"Is your number {guess}?"
    # This will return the updated state of each variable to be used in the next round of the game
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

    # This will be used for error handling if the user input is not valid
    try:
        #This will attempt to put arr variable to result of parsing the raw text input using the parse_array_text function. 
        # If the input is not valid, it will raise a ValueError
        arr = parse_array_text(raw_text)
    # If a ValueError is raised then it will set the game state to use the current array and prompt the user to enter a valid input.
    except ValueError:
        # low is set to 0
        low = 0
        # high is set to length of current array - 1 beccause the index starts at 0 so the last index is length - 1
        high = len(current_arr) - 1
        # Guess coun is set to 1 because we are making the first guess right after this function is called and if its 0 it will be a logical error
        guessCount = 0
        # mid is calculated based on adding low and high and then divide it by 2
        mid = (low + high) // 2
        # guess is set to the value at the mid index of the current array
        guess = current_arr[mid]
        # Message will be set to a string that prompts the user to enter a valid input of integers seprated by commas and also gives an example of how the input should look like
        message = "Invalid input. Use integers separated by commas, e.g. 3, 10, 2, 8"
        # This will return the current game state with the current array and the message prompting the user to enter a valid input
        return current_arr, low, high, guessCount, guess, message, mid, str(current_arr), message
    
    # All the variables init_state_from_array, guess_number, use_typed_array are called to generate a new random array and start the game with it.
    arr, low, high, guessCount, guess, message, mid = init_state_from_array(arr)
    #This will return the new game state with the new array and the message to ask user if this is their number
    return arr, low, high, guessCount, guess, message, mid, str(arr), message

# Define a function to generate a new random array and start the game with it.
# This function is only called when the user clicks the "Generate New Array" button and it will creata new random array
def generate_random_array():
    # All the variables init_state_from_array, guess_number, use_typed_array are called to generate a new random array and start the game with it.
    # they are being sent to the start function to generate a new random
    arr, low, high, guessCount, guess, message, mid = start()
    # This will return the new game state with new random array and the message to ask the user if this is their number
    return arr, low, high, guessCount, guess, message, mid, str(arr), message

# Define a function to start the game based on the user input. If the user has entered a valid array in the text box, it will use the array from the textbox to start the game.
def start_game(arr_text, current_arr):
    # If function is for checking if the user has entered a valid array in the text box. If the input is not empty or only contains white space, 
    # it will call the use_typed_array function to start the game with the user input array.
    if (arr_text or "").strip():
        # Return the result of use_typed_array function which will start the game with the user input array and also handle any errors if the input is not valid
        return use_typed_array(arr_text, current_arr)
    # If the user has not entered a valid array in the text box, it will call the generate_random_array function to start the game with a new random array.
    return generate_random_array()

# Define a function to handle the user input when they click the higher button. This function will update the game state based on the user input of higher
def on_higher(arr, low, high, guessCount, guess, message, mid):
    #This is just putting all the variables to the guess_number function to update the game state based on the user input of higher and then return the updated game state
    arr, low, high, guessCount, guess, message, mid = guess_number(
        # This will pass all the current game state variable to the guess number function to update the state based on the user input of higher
        arr, low, high, guessCount, guess, message, "Higher", mid
    )
    # This will return the updated game state along with the updated array and message to ask user if this is their number
    return arr, low, high, guessCount, guess, message, mid, str(arr), message

# Define a function to handle the user input when they click the lower button. This function will update the game state based on the user input of lower
def on_lower(arr, low, high, guessCount, guess, message, mid):
    #This is just putting all the variables to the guess_number function to update the game state based on the user input of lower and then return the updated game state
    arr, low, high, guessCount, guess, message, mid = guess_number(
        # This will pass all the current game state variable to the guess number function to update the state based on the user input of lower
        arr, low, high, guessCount, guess, message, "Lower", mid
    )
    # This will return the updated game state along with the updated array and message to ask user if this is their number 
    return arr, low, high, guessCount, guess, message, mid, str(arr), message

# Define a function to handle the user input when they click the complete button. This function will update the game state based on the user input of complete
def on_complete(arr, low, high, guessCount, guess, message, mid):
    #This is just putting all the variables to the guess_number function to update the game state based on the user input of complete and then return the updated game state
    arr, low, high, guessCount, guess, message, mid = guess_number(
        # This will pass all the current game state variable to the guess number function to update the state based on the user input of correct
        arr, low, high, guessCount, guess, message, "Correct", mid
    )
    # This will return the updated game state along with the updated array and message to ask user if this is their number and also a congratulatory message if the user has found their number
    return arr, low, high, guessCount, guess, message, mid, str(arr), message

#All the history of what player did and the result of that action will be stored in history variable and this function will be used to append new actions and messages to the history 
def append_history(history, action, message):
    # The line variable is a f string that combines the action and the message
    line = f"{action}: {message}"
    # If function is used to check the the history variable has any previous history, if it does then it will append the new line to the existing history
    if history:
        # This will return the existing history with a new line and the new action and message appended to it
        return f"{history}\n{line}"
    # This will return a new line
    return line

#This function is used to reset the history when the user starts a new game or generates a new array then it will clear the history and start fresh
def reset_history(action, message):
    # This will return a new line with the action and message to start the history fresh when the user starts a new game or generates a new array
    return f"{action}: {message}"

# Define a function to see if the user has clicked the start button. This function will check if the user has entered a valid array in the text box 
# and start the game with that array or generate a new random array if the input is not valid. It will also reset the history to start fresh for the new game.
def start_game_click(arr_text, current_arr, history):
    # This is calling the start_game function to check if the user has entered a valid array in the text box and start the game with that array
    arr, low, high, guessCount, guess, message, mid, arr_text_out, message_out = start_game(arr_text, current_arr)
    # This will reset the history to start fresh for the new game and also add a line to the history with the action of starting the game
    history_out = reset_history("Start", message_out)
    # This will return the updated game state along with the updated array and message to ask user if this is their number and also the reset history for the new game
    return arr, low, high, guessCount, guess, message, mid, arr_text_out, message_out, history_out, history_out

# Define a function to see if the user has clicked the "Use typed array" button. This function will check 
def use_typed_array_click(arr_text, current_arr, history):
    # These all values are being set to the result of the use_typed_array function which will check if the user has entered a valid array in the text box and start the game
    arr, low, high, guessCount, guess, message, mid, arr_text_out, message_out = use_typed_array(arr_text, current_arr)
    # This will reset the history to start fresh for the new game and also add a line to the history with the action of using a typed array
    history_out = reset_history("Use Typed Array", message_out)
    # This will return the updated game state along with the updated array and message to ask user if this is their number and also the reset history for the new game
    return arr, low, high, guessCount, guess, message, mid, arr_text_out, message_out, history_out, history_out

# Define a generate_random_array_click function to  see if the user clicked the generate random array button 
def generate_random_array_click(history):
    #This puts all the variables to the result of the generate_random_array function which will generate a new random array and start the game
    arr, low, high, guessCount, guess, message, mid, arr_text_out, message_out = generate_random_array()
    # This will reset the history to start fresh for the new game and also add line to the history with the action of generating a new random array
    history_out = reset_history("Generate New Array", message_out)
    # This will return the updated game state along with the updated array
    return arr, low, high, guessCount, guess, message, mid, arr_text_out, message_out, history_out, history_out

# Define a function to handle the user input when they click the higher button
def on_higher_click(arr, low, high, guessCount, guess, message, mid, history):
    # All the variables are being set to the result of the on_higher function which will update the game state based on the user input of higher and then return the updated game state
    arr, low, high, guessCount, guess, message, mid, arr_text_out, message_out = on_higher(
        # This will pass all the current game state variable on the higher function to update the state
        arr, low, high, guessCount, guess, message, mid
    )
    # This will put history_out to result to append_history function which will take the current history and add a new line with the action of higher and the 
    # message that was generated from the on_higher function
    history_out = append_history(history, "Higher", message_out)
    # This will return the updated game state along with the updated history that includes the new action and the messaged
    return arr, low, high, guessCount, guess, message, mid, arr_text_out, message_out, history_out, history_out

# Define a function to handle the user input when they click the lower button
def on_lower_click(arr, low, high, guessCount, guess, message, mid, history):
    # All the variables are being set to on_lower function which will update the game state based on the user input of lower and then return the updated game state
    arr, low, high, guessCount, guess, message, mid, arr_text_out, message_out = on_lower(
        # This will pass all the current game state variable on the lower function to update the state based on the user input of lower
        arr, low, high, guessCount, guess, message, mid
    )
    # This will put history_out to the result to append history function which will take the current history and add new line with the action
    history_out = append_history(history, "Lower", message_out)
    # This will return the updated game state along with the updated history that includes the new action and message
    return arr, low, high, guessCount, guess, message, mid, arr_text_out, message_out, history_out, history_out

# Define a function to handle the user input when they click the correct button. This function will update the game state to reflect that the user has found their number and it will also be updated in the history
def on_complete_click(arr, low, high, guessCount, guess, message, mid, history):
    # This will call the on_complete function to update the game state to reflect that the user has found their number and it will also update the messahe to congratulate the userand tell them how many guesses it took to find the number
    arr, low, high, guessCount, guess, message, mid, arr_text_out, message_out = on_complete(
        # This will pass all the current game state variables to the on_complete function to update the state based on the user input of correct
        arr, low, high, guessCount, guess, message, mid
    )

    # This will put history_out to the result to append_history function which will take the current history and add a new line with the action
    history_out = append_history(history, "Correct", message_out)
    # This will return the updated game state along with the updated history that includes the new action and message
    return arr, low, high, guessCount, guess, message, mid, arr_text_out, message_out, history_out, history_out

with gr.Blocks() as demo:
    initial_arr, initial_low, initial_high, initial_guess_count, initial_guess, initial_message, initial_mid = start()
    initial_history = f"Init: {initial_message}"

    # Define the state variable for the game state and initialize it with the initial values from the start function. 
    # These state variables will be used to keep track of the current game state and update it based on user interactions.
    arr = gr.State(initial_arr)
    low = gr.State(initial_low)
    high = gr.State(initial_high)
    guessCount = gr.State(initial_guess_count)
    guess = gr.State(initial_guess)
    message = gr.State(initial_message)
    mid = gr.State(initial_mid)
    history = gr.State(initial_history)
    
      #This will make the title and instructions for the game using markdown
    gr.Markdown("### Binary Search Game")
    gr.Markdown("Think of a number in the array and I will try to guess it. After each guess, tell me if your number is Higher or Lower than my guess.")
    
    # This will create a new row in gradio layout and inside that row it will create two text boxes with Array and Result label
    with gr.Row(equal_height=True):
        # This will create a textbox for the array input and display the current array that the game is using.
        # This will also let user input numbers in the textbox to start the game with a custom array
        arr_display = gr.Textbox(
            value=str(initial_arr),
            label="Array (comma-separated integers)",
            interactive=True,
            lines=2,
            scale=1,
        )
        # This will just display results of the game and the messages to the user.
        message_display = gr.Textbox(
            value=initial_message,
            label="Result",
            interactive=False,
            lines=2,
            scale=1,
        )
    
    # This will create a textbox to display the history of the game which will show the actions taken by the user and messages that are generated 
    history_display = gr.Textbox(
        value=initial_history,
        label="History",
        interactive=False,
        lines=10,
    )
    
    # This will create a row for the button and inside that row it will create 3 buttons for higher, lower, and correct. These button will use on
    # on_higher_click, on_lower_click, and on_complete_click functions to update the game state based on the user input of higher, lower, and correct
    with gr.Row():
        # Creating the button for higher, lower, and correct and labeling
        higher_button = gr.Button("Higher")
        lower_button = gr.Button("Lower")
        complete_button = gr.Button("Correct")

    # This is an intractive button when clicked it will call the on_higher_click function to update the 
    # game state based on the user input of higher and then return the updated game state along with the updated array
    higher_button.click(
        on_higher_click,
        # This will take all the inputes from the current game state and pass it to the on_higher_click function to update the state based on the user input of higher
        inputs=[arr, low, high, guessCount, guess, message, mid, history],
        # This will return the updated game state along with the updated array and message
        outputs=[arr, low, high, guessCount, guess, message, mid, arr_display, message_display, history, history_display],
    )

    # This will create a row for the start, use typed array, and generate new array buttons. 
    # These buttons will use start_game_click, use_typed_array_click, and generate_random_array_click functions to start the game based on user input
    with gr.Row():
        start_button = gr.Button("Start")
        use_typed_button = gr.Button("Use Typed Array")
        generate_button = gr.Button("Generate New Array")

    # This is an intractive button when clicked it will call the start_game_click function to update the 
    start_button.click(
        start_game_click,
        # This will take the input from the array text box and the current array state and pass it to the start_game_click function to check if 
        # the user has entered a valid array and start the game with that array or generate a new random array
        inputs=[arr_display, arr, history],
        # This will return the updated game state along with the updated array and message to ask user if this is their number and also the reset history for the new game
        outputs=[arr, low, high, guessCount, guess, message, mid, arr_display, message_display, history, history_display],
    )

    # This will create a row to start the game with user input array when user clicks the "Use Typed Array"
    # It will call the use_typed_array_click function to check if the user has entered a valid array in the text box and start the game
    use_typed_button.click(
        use_typed_array_click,
        # This will take the input from the array text box and the current array state and pass it to the use_typed_array_click function to check if
        # the user input is valid and start the game with that array
        inputs=[arr_display, arr, history],
        # This will display the array and message to ask user if this is their number and also the reset history for the new game 
        # if the input is valid or an error message if the input is not valid
        outputs=[arr, low, high, guessCount, guess, message, mid, arr_display, message_display, history, history_display],
    )

    # This will create an intractive button when clicked it will call the generate_random_array_click function
    # This will generate a new array randomly and start the game
    generate_button.click(
        generate_random_array_click,
        # This will only go to history because the generate_random_array_click function does not need any input to generate a new random array and start the game
        inputs=[history],
        # This will return the updated array and message to ask user if this is their number and also reset the history for the new game
        outputs=[arr, low, high, guessCount, guess, message, mid, arr_display, message_display, history, history_display],
    )

    # This will call the function on_complete_click when the user is clicked to tell the program to stop the game
    complete_button.click(
        on_complete_click,
        # This will take all the inputes from the current game state and pass it to the on_complete_click function
        # Tell the program that user has found the number and stop the game
        inputs=[arr, low, high, guessCount, guess, message, mid, history],
        # This will just update the game state to show that user has found the number and stop the game
        outputs=[arr, low, high, guessCount, guess, message, mid, arr_display, message_display, history, history_display],
    )

    # This will create an intractive button when clicked it will call the on_lower_click function
    lower_button.click(
        on_lower_click,
        # This will update the game state based on the user input of lower and then return the updated game state along with the updated array and message
        inputs=[arr, low, high, guessCount, guess, message, mid, history],
        # This will return the updated game state along with the updated array and message in the history
        outputs=[arr, low, high, guessCount, guess, message, mid, arr_display, message_display, history, history_display],
    )

    gr.Markdown("Click Generate New Array to start with a new random array or type your own array in the text box and click Use Typed Array to start with your custom array. ")
    gr.Markdown("It will sort the array automatically. and then the program will make a guess and ask you if this is your number.")
    gr.Markdown("Then use the Higher, Lower, and Correct buttons to play the game and see the history of your actions and results in the History box.")
    gr.Markdown("Remove the [] from the array input if you want to enter a custom array. For example, you can enter 3, 10, 2, 8 to create an array with those numbers.")
    gr.Markdown("Have fun playing the Binary Search Game and see how many guesses it takes to find your number!")


# Launch the Gradio app and share it with a public link so that anyone can access it and play the game
demo.launch(share=True) 
