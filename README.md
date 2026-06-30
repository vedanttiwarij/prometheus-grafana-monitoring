# 📊 Prometheus + Grafana Monitoring Stack

A fully containerized observability project that monitors a live Flask application using **Prometheus** for metrics collection and **Grafana** for real-time visualization — orchestrated entirely with **Docker Compose**.

## 🎯 What this project demonstrates

- Instrumenting an application with custom metrics (request counts, latency)
- Setting up Prometheus to scrape metrics from a live service
- Building real-time Grafana dashboards on top of that data
- Multi-container orchestration using Docker Compose
- Debugging real-world deployment issues (Docker daemon, networking, version conflicts)

## 🏗️ Architecture

```
┌─────────────┐       scrapes       ┌─────────────┐       queries      ┌─────────────┐
│  Flask App  │ ◄────────────────── │  Prometheus │ ◄───────────────── │   Grafana   │
│ (port 5000) │      every 15s      │ (port 9090) │                    │ (port 3000) │
└─────────────┘                     └─────────────┘                    └─────────────┘
```

The Flask app exposes a `/metrics` endpoint in Prometheus format. Prometheus scrapes this endpoint on a fixed interval and stores the time-series data. Grafana then queries Prometheus and renders that data as live dashboards.

## 🛠️ Tech Stack

- **Flask** — sample application being monitored
- **prometheus_client** (Python) — for exposing custom metrics
- **Prometheus** — metrics collection and storage
- **Grafana** — dashboarding and visualization
- **Docker & Docker Compose** — containerization and orchestration

## 📁 Project Structure

```
monitoring-project/
├── app/
│   ├── app.py            # Flask app with Prometheus instrumentation
│   ├── requirements.txt
│   └── Dockerfile
├── prometheus.yml         # Prometheus scrape configuration
├── docker-compose.yml     # Orchestrates all 3 services
└── README.md
```

## 🚀 How to Run

**Prerequisites:** Docker & Docker Compose installed and running.

```bash
git clone https://github.com/vedanttiwarij/prometheus-grafana-monitoring.git
cd prometheus-grafana-monitoring
docker-compose up --build
```

Once running, access:

| Service    | URL                     | Notes                  |
|------------|--------------------------|-------------------------|
| Flask App  | http://localhost:5000   | `/`, `/books`, `/slow`  |
| Prometheus | http://localhost:9090   | Check targets at `/targets` |
| Grafana    | http://localhost:3000   | Login: `admin` / `admin` |

## 📈 Custom Metrics Implemented

- `app_requests_total` — Counter tracking total requests, labeled by method and endpoint
- `app_request_latency_seconds` — Histogram tracking response time distribution per endpoint

## 🖼️ Screenshots

### Flask App Running
![App Home](screenshots/1-app-home.png)

### Raw Prometheus Metrics Endpoint
![Metrics Endpoint](screenshots/2-metrics-endpoint.png)

### Prometheus Target Health
![Prometheus Targets](screenshots/3-prometheus-targets.png)

### Grafana Real-Time Dashboard
![Grafana Dashboard](screenshots/5-grafana-dashboard.png)

## 🐛 Challenges Faced & Solutions

- **Docker daemon not running** — `docker-compose up` failed silently with a pipe connection error until Docker Desktop was properly started; resolved by ensuring the daemon was active before running commands.
- **Obsolete `version` attribute** — Docker Compose flagged the `version: '3.8'` key as obsolete in newer versions; removed it for forward compatibility.
- **Service discovery in Grafana** — Initially attempted to connect Grafana to Prometheus using `localhost:9090`, which fails inside a container network. Fixed by using the Docker Compose service name (`http://prometheus:9090`) instead, relying on Docker's internal DNS.

## 🔭 Future Improvements

- Add Alertmanager for threshold-based alerts (e.g., Slack notification on high latency)
- Add `node-exporter` for host-level system metrics (CPU, memory, disk)
- Deploy the same stack on Kubernetes (EKS) instead of Docker Compose

## 👤 Author

**Vedant Tiwari** — Self-taught DevOps Engineer
- GitHub: [@vedanttiwarij](https://github.com/vedanttiwarij)
- Instagram/YouTube: [@skycodes10](https://instagram.com/skycodes10)
