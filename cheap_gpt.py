import json
import time
import random
from http.server import BaseHTTPRequestHandler, HTTPServer

# Hardcoded dictionary to hold terms and responses
response_dict = {
    "flashing red light": (
        "<p>If you notice a flashing red light on your device, it is important to take immediate action to address the issue.</p>"
        "<p>This flashing light often indicates that there is a problem that needs to be resolved, and ignoring it could lead to further complications.</p>"
        "<p>To begin troubleshooting, unplug the device from the power source, wait for at least 30 seconds, and then plug it back in to see if the issue persists.</p>"
        "<p>After reconnecting the device, observe whether the red light continues to flash or if it returns to a normal state.</p>"
        "<p>If the light remains flashing, it may be necessary to consult the user manual or contact customer support for further assistance.</p>"
        "<p>In some cases, a flashing red light can signify a hardware failure, so it is crucial to address the situation promptly.</p>"
    ),
    "device not responding": (
        "<p>When your device is not responding, it can be incredibly frustrating, especially if you rely on it for important tasks.</p>"
        "<p>The first step in resolving this issue is to try restarting the device, as this can often clear temporary glitches that may be causing the unresponsiveness.</p>"
        "<p>To restart the device, press and hold the power button until it turns off, then wait a few moments before turning it back on.</p>"
        "<p>If the device still does not respond after restarting, consider checking for any software updates that may be available.</p>"
        "<p>Outdated software can sometimes lead to performance issues, so keeping your device updated is essential for optimal functionality.</p>"
        "<p>If the problem persists, it may be necessary to perform a factory reset, but be sure to back up any important data before doing so.</p>"
    )
}


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        response_message = self.check_for_terms(post_data)
        self.stream_response_with_possible_zeroes(response_message)

    def stream_infinite_zeroes(self):
        chunk_size = 1024  # 1KB chunks
        while True:
            try:
                self.wfile.write(b'0' * chunk_size)
                time.sleep(0.1)  # Small delay to prevent overwhelming the connection
            except (BrokenPipeError, ConnectionResetError):
                break

    def stream_response_with_possible_zeroes(self, response_message):
        response_data = {
            "timestamp": int(time.time()),
            "response": response_message
        }

        response_json = json.dumps(response_data)
        response_bytes = response_json.encode('utf-8')

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        chunk_size = len(response_bytes) // 10

        # Randomly decide if we'll switch to zeroes
        will_switch_to_zeroes = random.random() < 0.5
        # Randomly choose when to switch (between chunk 3 and 7)
        switch_at_chunk = random.randint(3, 7) if will_switch_to_zeroes else 11

        for i in range(10):
            if i == switch_at_chunk:
                # Switch to infinite zeroes
                self.stream_infinite_zeroes()
                return  # This will never be reached due to infinite loop

            # Stream normal chunk
            start_index = i * chunk_size
            end_index = start_index + chunk_size if i < 9 else len(response_bytes)
            self.wfile.write(response_bytes[start_index:end_index])
            time.sleep(1.0)

    def check_for_terms(self, post_data):
        for term, response in response_dict.items():
            if term in post_data:
                return response
        return "No matching terms found."


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8081):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()


if __name__ == "__main__":
    run()
