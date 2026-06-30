from flask import Flask
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import random
import time

app = Flask(__name__)

# Counter: sirf badhta hai, kabhi kam nahi hota (jaise total request count)
REQUEST_COUNT = Counter(
    'app_requests_total',          # metric ka naam
    'Total number of requests',    # description (help text)
    ['method', 'endpoint']         # labels -- inse hum data ko filter/group kar sakte hain
)

# Histogram: response time jaisi cheez ke liye, jisme distribution important hai
REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds',
    'Request latency in seconds',
    ['endpoint']
)


@app.route('/')
def home():
    start_time = time.time()

    # Real app jaisa simulate karne ke liye random delay
    time.sleep(random.uniform(0.05, 0.3))

    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()  # counter ko 1 se badhao
    REQUEST_LATENCY.labels(endpoint='/').observe(time.time() - start_time)

    return "Welcome to the Monitored App! Try /books or /slow"


@app.route('/books')
def books():
    start_time = time.time()
    time.sleep(random.uniform(0.1, 0.5))

    REQUEST_COUNT.labels(method='GET', endpoint='/books').inc()
    REQUEST_LATENCY.labels(endpoint='/books').observe(time.time() - start_time)

    return {"books": ["Atomic Habits", "Deep Work", "Sapiens"]}


@app.route('/slow')
def slow():
    # Jaanbujhke slow endpoint -- baad mein dekhenge ki Grafana mein
    # latency spike kaise dikhta hai
    start_time = time.time()
    time.sleep(random.uniform(1, 2.5))

    REQUEST_COUNT.labels(method='GET', endpoint='/slow').inc()
    REQUEST_LATENCY.labels(endpoint='/slow').observe(time.time() - start_time)

    return "That was slow on purpose!"


@app.route('/metrics')
def metrics():
    # Yeh wahi endpoint hai jo Prometheus scrape karega
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
