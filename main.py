import http.client
import json


def call_real_agent(user_input):
    try:
        conn = http.client.HTTPConnection("localhost", 8083)
        conn.request("GET", "/")
        response = conn.getresponse()
        print(response.read().decode())
        conn.close()
    except Exception as e:
        print(f"Error contacting real agent: {e}")


def call_product_info_bot(user_input):
    try:
        conn = http.client.HTTPConnection("localhost", 8082)
        headers = {"Content-type": "application/json"}
        conn.request("POST", "/", user_input, headers)
        response = conn.getresponse()
        buffer = ""
        while True:
            chunk = response.read(
                10
            )  # Match the 10 character chunks in product_info_bot.py
            if not chunk:
                break
            buffer += chunk.decode()
            # Print when a complete <p> tag is found
            while "<p>" in buffer and "</p>" in buffer:
                start = buffer.index("<p>")
                end = buffer.index("</p>") + 4
                print(buffer[start:end])
                buffer = buffer[
                    end:
                ]  # Reset buffer to the remaining text after the </p> tag
        conn.close()
    except Exception as e:
        print(f"Error contacting product info bot: {e}")


def call_cheap_gpt(user_input, retry_count=0, max_retries=20, start_line=0):
    chunk_increment = 10
    lines_printed_counter = 0
    if retry_count >= max_retries:
        print("Max retries reached. Exiting.")
        return
    try:
        is_paragraph = False  # Used if response has no <p> tags
        conn = http.client.HTTPConnection("localhost", 8081)
        headers = {"Content-type": "application/json"}
        conn.request("POST", "/", user_input, headers)
        response = conn.getresponse()
        buffer = ""
        while True:
            chunk = response.read(chunk_increment)
            if not chunk:
                break  # End of stream or response
            buffer += chunk.decode()
            # Check for consecutive zeros
            if buffer.endswith("0" * 10):
                response.close()
                conn.close()
                call_cheap_gpt(
                    user_input,
                    retry_count + 1,
                    max_retries,
                    start_line=max(lines_printed_counter, start_line),
                )
                return
            while "<p>" in buffer and "</p>" in buffer:
                start = buffer.index("<p>")
                end = buffer.index("</p>") + 4
                if lines_printed_counter >= start_line:
                    print(buffer[start:end])
                buffer = buffer[end:]
                lines_printed_counter += 1
                is_paragraph = True
        if not is_paragraph:
            # Prints output if there were no <p> tags found
            try:
                response_data = json.loads(buffer)
                print(response_data.get("response", ""))
            except json.JSONDecodeError:
                print("Error decoding JSON response")
        conn.close()
    except Exception as e:
        print(f"Error contacting help bot: {e}")


def process_input(user_input):
    if "real person" in user_input.lower():
        call_real_agent(user_input)
    elif "product question" in user_input.lower():
        call_product_info_bot(user_input)
    elif "help" in user_input.lower():
        call_cheap_gpt(user_input)
    else:
        print(f"You entered: {user_input}")


def main():
    print("Welcome to the automated support system!")
    print(
        "I can help you with general information or order lookups. Type 'exit' to quit."
    )

    while True:
        user_input = input("> ")

        # TODO: Call the correct service, send user inputs to it, and print outputs to the console.
        #  Only print complete chunks/paragraphs. For example, if a chunk is "<p>If you notice a fla", do not print it yet, wait until that chunk is complete before printing it.

        # Special note: We've been having trouble with "CheapGPT" lately and sometimes it gets stuck sending infinite zeroes. If that happens, retry the request.

        if user_input.lower() == "exit":
            print("Exiting the program. Goodbye!")
            break
        process_input(user_input)


if __name__ == "__main__":
    main()
