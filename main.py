def process_input(user_input):
    # This function processes the user input.
    # You can modify this function to perform any action you want.
    print(f"You entered: {user_input}")


def main():
    print("Welcome to the automated support system!")
    print("I can help you with general information or order lookups. Type 'exit' to quit.")

    while True:
        user_input = input("> ")

        # TODO: Call the correct service, send user inputs to it, and print outputs to the console.
        #  Only print complete chunks/paragraphs. For example, if a chunk is "<p>If you notice a fla", do not print it yet, wait until that chunk is complete before printing it.

        # Special note: We've been having trouble with "CheapGPT" lately and sometimes it gets stuck sending infinite zeroes. If that happens, retry the request.

        if user_input.lower() == 'exit':
            print("Exiting the program. Goodbye!")
            break
        process_input(user_input)


if __name__ == "__main__":
    main()
