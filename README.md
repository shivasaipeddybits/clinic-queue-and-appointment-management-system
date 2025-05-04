## Clinic Appointment System - Microservices Architecture
This project is a clinic appointment and notification system built using FastAPI and PostgreSQL, structured as independent microservices. Each service is Dockerized and can be scaled independently.

##### Services Overview

- **Frontend Service**: Handles user interface (HTML forms).

- **Patient Service**: Registers and verifies patients.

- **Doctor Service**: Registers and lists doctors.

- **Appointment Service**: Books and lists appointments.

- **Notification Service**: Sends email notifications via Mailgun.

- **PostgreSQL Database**: Stores shared data (used by services via isolated schemas or joined views).

##### Dockerized Setup
**Prerequisites**
- Docker
- Docker Compose
- .env files with proper configuration (e.g., **API_KEY** for Mailgun)

