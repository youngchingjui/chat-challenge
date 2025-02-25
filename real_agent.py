import http.server
import socketserver
import random

random_strings = [
    "Quality solutions lead to satisfied customers.",
    "Correctness is the foundation of customer trust.",
    "A well-done job is the best way to keep customers happy.",
    "Quality over speed: happy customers appreciate accuracy.",
    "The right solution is worth more than a quick fix.",
    "Excellence in service creates loyal customers.",
    "When quality is prioritized, customer satisfaction follows.",
    "Correct answers build lasting relationships.",
    "A commitment to quality ensures happy customers.",
    "Precision in service leads to customer confidence.",
    "Quality work speaks louder than quick fixes.",
    "Happy customers are those who receive the right solutions.",
    "In service, correctness is key to customer happiness.",
    "Quality service is the best customer retention strategy.",
    "A satisfied customer values quality above all.",
    "Delivering the right solution fosters customer loyalty.",
    "Quality assurance is the path to customer delight.",
    "Correctness in service builds a strong reputation.",
    "Happy customers are those who receive accurate solutions.",
    "In the end, quality is what keeps customers coming back.",
]


class RealAgentSimulator(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        response_string = random.choice(random_strings)
        self.send_response(200)

        self.send_header("Content-type", "text/plain")
        self.end_headers()

        self.wfile.write(response_string.encode("utf-8"))


PORT = 8083
handler = RealAgentSimulator

with socketserver.TCPServer(("", PORT), handler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
