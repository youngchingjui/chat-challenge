import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

# Product information dictionary
product_dict = {
    "Space Basketball": (
        "<p>Extra bouncy basketball in neon green that glows in the dark.</p>"
        "<p>Excellent for playing in dark areas like outer space.</p>"
        "<p>WARNING: Not suitable for use outside of Earth.</p>"
    ),
    "Quantum Coffee Maker": (
        "<p>Revolutionary coffee maker that brews your coffee in multiple dimensions simultaneously.</p>"
        "<p>Every cup tastes like it was made in a parallel universe where you're a master barista.</p>"
        "<p>NOTE: May occasionally create temporal coffee stains.</p>"
    ),
    "Telepathic Toaster": (
        "<p>Smart toaster that reads your mind to determine the perfect toasting level.</p>"
        "<p>Includes AI-powered bread recognition and interdimensional crumb tray.</p>"
        "<p>CAUTION: May pick up breakfast desires from neighbors within 50 feet.</p>"
    ),
    "Antigravity Socks": (
        "<p>Self-levitating socks that float gently in your drawer.</p>"
        "<p>Never lose a sock again - they actively seek their matching pair!</p>"
        "<p>WARNING: Do not wear during thunderstorms or solar flares.</p>"
    ),
    "Time Travel Alarm Clock": (
        "<p>Alarm clock that lets you snooze by temporarily reversing time by 5 minutes.</p>"
        "<p>Perfect for chronic oversleepers.</p>"
        "<p>DISCLAIMER: May cause mild temporal jet lag.</p>"
    )
}


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        response_message = self.check_for_product(post_data)
        self.stream_response_in_chunks(response_message)

    def stream_response_in_chunks(self, response_message):
        response_data = {
            "timestamp": int(time.time()),
            "product_info": response_message
        }

        response_json = json.dumps(response_data)
        response_bytes = response_json.encode('utf-8')

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        chunk_size = len(response_bytes) // 10

        for i in range(10):
            start_index = i * chunk_size
            end_index = start_index + chunk_size if i < 9 else len(response_bytes)
            self.wfile.write(response_bytes[start_index:end_index])
            time.sleep(1.0)

    def check_for_product(self, post_data):
        for product, info in product_dict.items():
            if product in post_data:
                return info
        return "<p>Product not found in catalog.</p>"


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8082):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()


if __name__ == "__main__":
    run()
