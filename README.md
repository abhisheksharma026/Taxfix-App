This repository contains a FastAPI application that predicts whether the user completed the tax filing process or not.

📌 Features

- ✅ FastAPI-based API service for tax filing predictions.
- ✅ Model trained using CatBoost and stored in models/catboost_model.pkl.
- ✅ Uses Poetry for dependency management.
- ✅ Dockerized for deployment using Docker Compose.

📂 Project Structure
```javascript
TaxFix-App/
│-- app.log                     # Application logs 
│-- data/                        # Data folder (ignored in Git) 
│-- models/                      # Trained model files (ignored in Git)
│   ├── catboost_model.pkl       # Trained CatBoost model
│-- config.py                    # Configuration settings
│-- preparation.py                # Feature processing logic
│-- model.py                      # Model training and evaluation
│-- model_service.py              # Model loading and prediction service
│-- runner.py                     # Script to test model predictions
│-- inference.py                  # FastAPI prediction endpoint
│-- Dockerfile                    # Docker container setup
│-- docker-compose.yml            # Docker Compose setup
│-- poetry.lock                   # Poetry lock file
│-- pyproject.toml                # Poetry dependencies
│-- README.md                     # Project documentation
│-- .gitignore                     # Ignore unnecessary files in Git
```


🐳 Run with Docker

1️⃣ Build & Run the Docker Container
- docker-compose up --build
2️⃣ Test the API
- curl -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d @test_input.json

To run FastAPI Locally
FastAPI will be accessible at:
- 📌 Swagger UI: http://127.0.0.1:8000/docs
- 📌 Redoc UI: http://127.0.0.1:8000/redoc
- command: uvicorn inference:app --host 0.0.0.0 --port 8000 --reload

📝 Example API Request

POST request to /predict with the following JSON body:
```javascript
{
    "age": 30,
    "income": 45000,
    "employment_type": "full_time",
    "marital_status": "single",
    "time_spent_on_platform": 120,
    "number_of_sessions": 5,
    "fields_filled_percentage": 80,
    "previous_year_filing": 1,
    "device_type": "mobile",
    "referral_source": "friend_referral"
}
```

### Possible Next Steps for a complete application workflow:

#### Automate the Development Workflow with GitHub Actions
- Implement CI/CD pipeline for automated testing, building, and deployment.
- Run tests & linting on each pull request before merging.
- Push Docker images to AWS/GCP/Azure registry and deploy automatically

#### Implement Infrastructure as Code (IaC)
- Use Terraform or AWS CloudFormation to automate the provisioning of ECS clusters, API gateways, and load balancers.

#### Enhance Observability & Monitoring
- Add structured logging (e.g., JSON logs) using Loguru for better insights.
- Integrate monitoring tools:
    - Prometheus + Grafana for real-time API health tracking.
    - AWS CloudWatch / GCP Stackdriver for system performance.
    - Sentry / Datadog for application error tracking.
 
#### Add Rate Limiting & API Security
- Rate-limiting middleware (FastAPI-limiter + Redis).

#### Automate Model Monitoring & Retraining
- Set up drift detection using Evidently AI.
- Retrain models periodically using a scheduled CI/CD pipeline.
- Deploy new models incrementally with A/B testing before full rollout.

#### Improve Scalability & Resilience
- Use Kubernetes (EKS/GKE/AKS) instead of standalone Docker containers.
- Enable autoscaling policies for handling unpredictable traffic loads.
- Deploy API gateways & CDN caching for faster response times.

