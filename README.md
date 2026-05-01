# 🍔 Food Delivery System

A microservices-based food delivery backend built with **Flask**, **Docker**, **RabbitMQ**, **Prometheus**, **Grafana**, and **Kubernetes**.

---

## 📐 Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Kubernetes / Docker                │
│                                                      │
│  ┌─────────────┐        ┌──────────────────────┐    │
│  │ user-service│        │  restaurant-service  │    │
│  │  Port 5000  │        │     Port 5000        │    │
│  └─────────────┘        └──────────────────────┘    │
│                                                      │
│  ┌─────────────┐        ┌──────────────────────┐    │
│  │order-service│──────▶│   payment-service    │    │
│  │  Port 5000  │RabbitMQ│     Port 5000        │    │
│  └─────────────┘        └──────────────────────┘    │
│                                                      │
│  ┌──────────┐  ┌────────────┐  ┌────────────────┐   │
│  │ RabbitMQ │  │ Prometheus │  │    Grafana     │   │
│  │ 5672     │  │   9090     │  │    3000        │   │
│  └──────────┘  └────────────┘  └────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## 🧩 Services

| Service | Port | Description |
|---|---|---|
| `user-service` | 5001 | Register and list users |
| `restaurant-service` | 5002 | Manage restaurants and menus |
| `order-service` | 5003 | Place orders, publish to RabbitMQ |
| `payment-service` | 5004 | Process payments, consume from RabbitMQ |
| `rabbitmq` | 5672 / 15672 | Message broker between order & payment |
| `prometheus` | 9090 | Metrics collection |
| `grafana` | 3000 | Metrics visualization |

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Minikube (for Kubernetes)
- kubectl

---

## 🐳 Docker Compose

### Development
```bash
docker-compose -f docker-compose.dev.yml up --build
```

### Staging
```bash
docker-compose -f docker-compose.staging.yml up --build
```

### Production
```bash
docker-compose -f docker-compose.prod.yml up --build
```

| Environment | User | Restaurant | Order | Payment |
|---|---|---|---|---|
| Development | 5001 | 5002 | 5003 | 5004 |
| Staging | 6001 | 6002 | 6003 | 6004 |
| Production | 7001 | 7002 | 7003 | 7004 |

---

## ☸️ Kubernetes (Minikube)

### 1. Start Minikube
```bash
minikube start
```

### 2. Build images inside Minikube (so it can find them)
```bash
eval $(minikube docker-env)

docker build -t food-delivery-system_user-service:latest ./user-service
docker build -t food-delivery-system_restaurant-service:latest ./restaurant-service
docker build -t food-delivery-system_order-service:latest ./order-service
docker build -t food-delivery-system_payment-service:latest ./payment-service
```

### 3. Apply all manifests
```bash
kubectl apply -f k8s/
```

### 4. Check everything is running
```bash
kubectl get pods
kubectl get services
```

### 5. Access the services
```bash
# User Service
minikube service user-service --url

# Or port-forward manually
kubectl port-forward svc/user-service 5001:5000
kubectl port-forward svc/restaurant-service 5002:5000
kubectl port-forward svc/order-service 5003:5000
kubectl port-forward svc/payment-service 5004:5000
kubectl port-forward svc/grafana 3000:3000
kubectl port-forward svc/prometheus 9090:9090
kubectl port-forward svc/rabbitmq 15672:15672
```

### 6. Enable Ingress (optional)
```bash
minikube addons enable ingress
kubectl apply -f k8s/ingress.yaml

# Add to /etc/hosts
echo "$(minikube ip) food-delivery.local" | sudo tee -a /etc/hosts
```

Then access: `http://food-delivery.local/users`, `/orders`, `/restaurants`, `/payments`

---

## 📡 API Endpoints

### User Service
```
POST /register     → Register a new user
GET  /users        → List all users
GET  /health       → Health check
```

**Example:**
```bash
curl -X POST http://localhost:5001/register \
  -H "Content-Type: application/json" \
  -d '{"name": "Yehia", "email": "yehia@example.com", "role": "customer"}'
```

---

### Restaurant Service
```
POST /restaurants                        → Add a restaurant
GET  /restaurants                        → List all restaurants
POST /restaurants/<id>/menu             → Add menu item
GET  /restaurants/<id>/menu             → Get menu
GET  /health                            → Health check
```

**Example:**
```bash
curl -X POST http://localhost:5002/restaurants \
  -H "Content-Type: application/json" \
  -d '{"name": "Pizza Palace", "cuisine": "Italian"}'
```

---

### Order Service
```
POST /orders          → Place an order (publishes to RabbitMQ)
GET  /orders          → List all orders
GET  /orders/<id>     → Get specific order
GET  /health          → Health check
```

**Example:**
```bash
curl -X POST http://localhost:5003/orders \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "restaurant_id": 1, "items": ["Pizza"], "total": 15.99}'
```

---

### Payment Service
```
GET  /payments    → List all payments
POST /pay         → Manual payment
GET  /health      → Health check
```

> 💡 Payments are also processed **automatically** via RabbitMQ when an order is placed.

---

## 🐇 RabbitMQ

- **Management UI:** http://localhost:15672 (guest / guest)
- **Queue:** `payment_queue`
- **Flow:** `order-service` publishes → `payment-service` consumes → payment auto-processed

---

## 📊 Monitoring

### Prometheus
- URL: http://localhost:9090
- Scrapes metrics from all 4 services every 15 seconds

### Grafana
- URL: http://localhost:3000
- Default credentials: `admin` / `admin`
- Add Prometheus as a data source: `http://prometheus:9090`

---

## 📁 Project Structure

```
food-delivery-system/
├── user-service/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── restaurant-service/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── order-service/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── payment-service/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── k8s/
│   ├── user-deployment.yaml
│   ├── restaurant-deployment.yaml
│   ├── order-deployment.yaml
│   ├── payment-deployment.yaml
│   ├── rabbitmq-deployment.yaml
│   ├── monitoring-deployment.yaml
│   └── ingress.yaml
├── docker-compose.dev.yml
├── docker-compose.staging.yml
├── docker-compose.prod.yml
├── prometheus.yml
└── README.md
```

---

## ✅ Features Checklist

- [x] 4 Flask Microservices
- [x] 4 Dockerfiles
- [x] Docker Compose (dev / staging / prod)
- [x] RabbitMQ message queue (order → payment)
- [x] Prometheus + Grafana monitoring
- [x] Kubernetes deployments with health checks & resource limits
- [x] Kubernetes Ingress
