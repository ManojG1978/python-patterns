from flask import Flask, jsonify
import os
from dotenv import load_dotenv
import random
import time
from color_print import print_info

app = Flask(__name__)

# Load environment variables
load_dotenv()
failure_rate = int(os.getenv('FAILURE_RATE', '0'))
max_response_time = int(os.getenv('MAX_RESPONSE_TIME_SECS', '5'))

@app.route('/')
def home():

    # introduce a random delay between 0 and MAX_RESPONSE_TIME_SECS seconds
    delay = random.randint(0, max_response_time)
    time.sleep(delay)
    print_info(f"Request processed after {delay} seconds.")

    # introduce a random failure rate
    if random.randint(1, 100) <= failure_rate:
        return jsonify({'message': 'Request failed due to configured failure rate.'}), 500
    else:
        return jsonify({'message': 'Request processed successfully.'})

if __name__ == '__main__':
    app.run(debug=True)
