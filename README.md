

# Two Way Strip Payment System Sync Project

  

This project is designed to synchronize CRM systems like Stripe, etc. Using FastAPI, SQLAlchemy, and Kafka with a PostgreSQL database.

  

## Prerequisites

  

Before you begin, ensure you have met the following requirements:

- Python 3.10.x

- PostgreSQL

- Docker (for containerization)

  

## Installation

  

1. Clone the repository:

```bash

git clone https://github.com/Siddharth-Xenon/Two-way-payment-integration.git

```

  

2. Install the required Python packages:

```bash

pip install -r requirements.txt

```

  

3. Set up your environment variables:

- Create a `.env` file in the root directory of your project.

- Fill in the `.env` file with your database credentials and Stripe API keys.

```bash

DB_USERNAME=

DB_PASSWORD=

DB_HOST=

DB_NAME=payments

DB_PORT=5432

STRIPE_API_KEY=

STRIPE_WEBHOOK_SECRET=
```

Fill in the `DB_USERNAME`, `DB_PASSWORD`, `DB_HOST`, `STRIPE_API_KEY`, and `STRIPE_WEBHOOK_SECRET` with your credentials.

  

## Database Setup

  

1. Ensure PostgreSQL is running on your system.

2. Create a database named `payments` or as specified in your `.env` file.

3. Run the database migrations:

```bash

alembic upgrade head

```

  

## Docker(Kafka) Setup

  

1. Start the Docker containers for the services:

```bash

docker-compose up -d

```

  

This command will start all the services defined in the `docker-compose.yml` file, including Kafka and Zookeeper, in detached mode.

  

## Ngrok

  

To expose your local Stripe server to the internet, use ngrok to create a public domain. This will allow Stripe to send webhook events to your local server:

  

1. Download and install ngrok from [ngrok.com](https://ngrok.com/).

  

2. Run ngrok to expose port 5000 (or the port your local server is running on):

```bash

ngrok http 5000

```

  

This command will output a public domain (e.g., `https://<random-id>.ngrok.io`). Note this domain as `<domain>`.

  

3. Create a webhook endpoint on your server that listens to `<domain>/webhook`. Ensure your server at this endpoint can handle POST requests and process the webhook data sent by Stripe.

  

4. Configure the webhook in your Stripe dashboard:

- Go to the [Stripe dashboard](https://dashboard.stripe.com/test/webhooks).

- Click on `+ Add endpoint`.

- Enter the URL `<domain>/webhook`.

- Select the events to listen to: `customer.created`, `customer.updated`, `customer.deleted`.

- Add the endpoint.

  

This setup will allow your local development environment to receive real-time notifications from Stripe about customer events.

  
  

## Running the Application

  

1. Start the FastAPI server:

```bash

uvicorn app.main:app --reload

```

  

This will start the server on `http://localhost:8000`. The `--reload` flag enables auto-reloading of the server when you make changes to the code.

  

2. Access the API documentation:

- Navigate to `http://localhost:8000/docs` in your web browser to view the Swagger UI documentation.

- Navigate to `http://localhost:8000/redoc` to view the Redoc documentation.
