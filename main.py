from flask import Flask, render_template, request, Response, stream_with_context
import json
import threading
import queue
import time
import re
from trace_engine import run_trace
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)
# Initialize Rate Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="memory://"
)

def clean_input(text):
    return re.sub(r'[^a-zA-Z0-9_.]', '', text)

@app.route('/', methods=['GET'])
def home():
    # Just render the empty page initially
    return render_template('index.html')

@app.route('/stream')
@limiter.limit("2 per minute")
def stream():
    username = request.args.get('username')
    if not username:
        return "Error: No username", 400
    
    username = clean_input(username)
    print(f"Starting scan for: {username}") # Debug log

    # A Queue to hold results as they come in
    result_queue = queue.Queue()

    # The callback that trace_engine will use
    def on_found(result):
        result_queue.put(result)

    # Run the scan in a separate thread so it doesn't block Flask
    def worker():
        try:
            run_trace(username, on_found)
        finally:
            # Put None to signal that the scan is done
            result_queue.put(None)

    threading.Thread(target=worker).start()

    # This Generator yields data to the browser line-by-line
    def generate():
        while True:
            item = result_queue.get()
            if item is None:
                # Send a "DONE" event
                yield f"data: {json.dumps({'status': 'done'})}\n\n"
                break
            
            # Send the found site as JSON
            yield f"data: {json.dumps(item)}\n\n"

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, threaded=True)
