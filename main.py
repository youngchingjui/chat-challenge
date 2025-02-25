import http.client
import json
from typing import Any

# Constants for configuration
CHUNK_SIZE = 10
MAX_RETRIES = 20


def call_real_agent(user_input: str) -> None:
    """Call the real agent service."""
    conn = http.client.HTTPConnection("localhost", 8083)
    try:
        conn.request("GET", "/")
        response = conn.getresponse()
        print(response.read().decode())
    except Exception as e:
        print(f"Error contacting real agent: {e}")
    finally:
        conn.close()


def call_streaming_server(
    user_input: str,
    port: int,
    retry_count: int = 0,
    max_retries: int = MAX_RETRIES,
    start_line: int = 0,
) -> None:
    """Call streaming service with retry logic."""
    if retry_count >= max_retries:
        print("Max retries reached. Exiting.")
        return
    conn = http.client.HTTPConnection("localhost", port)
    try:
        is_paragraph = False  # Print buffer if there were no <p> tags
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
            if buffer.endswith("0" * 10):  # Assume consecutive 10 x 0's means stuck
                response.close()
                conn.close()
                call_streaming_server(
                    user_input,
                    port,
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
    # real_agent uses simple GET request with `text/plain` response,
    # so we just separate it into its own function
    if "real person" in user_input.lower():
        call_real_agent(user_input)
        return

    port: int
    if "product question" in user_input.lower():
        port = 8082
    elif "help" in user_input.lower():
        port = 8081
    else:
        print(f"You entered: {user_input}")
        return

    call_streaming_server(user_input, port=port)


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
