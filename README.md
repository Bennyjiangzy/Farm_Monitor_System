# Farm Monitor System

This project was designed and developed based on microservice architecture. It has 5 parts. The business logic is that a receiver VM will receive data from outside. Then it will parse the data and store it in a database via a storage API. One processing API will periodically read and calculate the data via the storage API and store it in another database. One audit API can search data based on an index. Finally, all API statuses and any statistical data will be displayed on a UI dashboard that will refresh every 5 seconds. The whole project has been integrated into a CI/CD pipeline and a native Python logging system.

# Technologies used
- Python
- SwaggerHub and OpenAPI
- MySQL
- SQLite
- Kafka
- Docker
- Docker Compose
- jMeter
- Azure