import http.client
import json
from typing import Any

# Constants for configuration
REAL_AGENT_HOST = "localhost"
REAL_AGENT_PORT = 8083
PRODUCT_INFO_BOT_HOST = "localhost"
PRODUCT_INFO_BOT_PORT = 8082
CHEAP_GPT_HOST = "localhost"
CHEAP_GPT_PORT = 8081
CHUNK_SIZE = 10
MAX_RETRIES = 20


def call_real_agent(user_input: str) -> None:
    """Call the real agent service."""
    conn = http.client.HTTPConnection(REAL_AGENT_HOST, REAL_AGENT_PORT)
    try:
        conn.request("GET", "/")
        response = conn.getresponse()
        print(response.read().decode())
    except Exception as e:
        print(f"Error contacting real agent: {e}")
    finally:
        conn.close()


def call_product_info_bot(user_input: str) -> None:
    """Call the product info bot service."""
    conn = http.client.HTTPConnection(PRODUCT_INFO_BOT_HOST, PRODUCT_INFO_BOT_PORT)
    try:
        headers = {"Content-type": "application/json"}
        conn.request("POST", "/", user_input, headers)
        response = conn.getresponse()
        buffer = ""
        while True:
            chunk = response.read(CHUNK_SIZE)
            if not chunk:
                break
            buffer += chunk.decode()
            while "<p>" in buffer and "</p>" in buffer:
                start = buffer.index("<p>")
                end = buffer.index("</p>") + 4
                print(buffer[start:end])
                buffer = buffer[end:]
    except Exception as e:
        print(f"Error contacting product info bot: {e}")
    finally:
        conn.close()


def call_cheap_gpt(
    user_input: str,
    retry_count: int = 0,
    max_retries: int = MAX_RETRIES,
    start_line: int = 0,
) -> None:
    """Call the CheapGPT service with retry logic."""
    if retry_count >= max_retries:
        print("Max retries reached. Exiting.")
        return
    conn = http.client.HTTPConnection(CHEAP_GPT_HOST, CHEAP_GPT_PORT)
    try:
        is_paragraph = False
        headers = {"Content-type": "application/json"}
        conn.request("POST", "/", user_input, headers)
        response = conn.getresponse()
        buffer = ""
        lines_printed_counter = 0
        while True:
            chunk = response.read(CHUNK_SIZE)
            if not chunk:
                break  # End of stream or response
            buffer += chunk.decode()
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
            try:
                response_data = json.loads(buffer)
                print(response_data.get("response", ""))
            except json.JSONDecodeError:
                print("Error decoding JSON response")
    except Exception as e:
        print(f"Error contacting help bot: {e}")
    finally:
        conn.close()


def process_input(user_input: str) -> None:
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
