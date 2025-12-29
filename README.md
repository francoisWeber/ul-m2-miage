# Data Engineering Workshop Environment

A comprehensive, production-ready data engineering workshop environment for M2 MIAGE students, featuring modern data tools and real-world datasets.

## 🎯 Overview

This repository provides a complete data engineering stack using Docker Compose, designed for hands-on learning and experimentation with:

- **Relational Databases** (MySQL)
- **Distributed Processing** (Apache Spark)
- **Caching & Message Queues** (Redis)
- **Vector Databases** (Qdrant)
- **Search Engines** (Vespa)
- **Object Storage** (MinIO S3)
- **Interactive Development** (JupyterHub)

## 📊 Dataset

The workshop uses the **Open Beer Database** containing:
- 🍺 ~8,000 beers with detailed information (ABV, IBU, SRM)
- 🏭 ~1,500 breweries with geographic data
- 📂 Categories and styles classification
- ⭐ User feedback and ratings

## 🚀 Quick Start

### Prerequisites

- Docker (version 20.10+)
- Docker Compose (version 2.0+)
- At least 8GB RAM available for Docker
- 20GB free disk space

### Installation

1. **Clone the repository** (or copy files to the server):
```bash
cd /path/to/ul-m2-miage
```

2. **Run setup script**:
```bash
chmod +x scripts/*.sh
./scripts/setup.sh
```

3. **Start all services**:
```bash
./scripts/start.sh
```

4. **Access JupyterHub**:
   - Open http://localhost:8000 in your browser
   - Login with username: `admin` / password: `admin123`
   - Or create a new account (sign-up is enabled by default)

## 🔧 Services & Ports

| Service | Port | Web Interface | Description |
|---------|------|---------------|-------------|
| **JupyterHub** | 8000 | http://localhost:8000 | Main entry point for students |
| **Spark Master** | 8080 | http://localhost:8080 | Spark cluster management UI |
| **Spark Worker 1** | 8081 | http://localhost:8081 | Worker node UI |
| **Spark Worker 2** | 8082 | http://localhost:8082 | Worker node UI |
| **MySQL** | 3306 | - | Relational database |
| **Redis** | 6379 | - | In-memory data store |
| **Qdrant** | 6333 | http://localhost:6333/dashboard | Vector database |
| **Vespa** | 8088 | http://localhost:8088 | Search engine |
| **MinIO** | 9000, 9001 | http://localhost:9001 | S3-compatible storage |
| **Adminer** | 8089 | http://localhost:8089 | Database management UI |

## 📚 Workshop Notebooks

The `notebooks/` directory contains guided exercises:

1. **00_Welcome_and_Setup.ipynb** - Environment verification
2. **01_MySQL_Basics.ipynb** - SQL queries and relational data
3. **02_Spark_Processing.ipynb** - Distributed data processing
4. **03_Redis_Caching.ipynb** - Caching patterns and performance
5. **04_Qdrant_Vectors.ipynb** - Vector embeddings and semantic search
6. **05_S3_Storage.ipynb** - Object storage operations

Each notebook includes:
- ✅ Step-by-step instructions
- 💡 Practical examples
- 🎯 Hands-on exercises
- 📊 Data visualizations

## 🛠️ Management Scripts

All scripts are located in the `scripts/` directory:

```bash
# Setup environment and create .env file
./scripts/setup.sh

# Start all services
./scripts/start.sh

# Stop all services (preserves data)
./scripts/stop.sh

# Check service status and health
./scripts/status.sh

# View logs for specific service
./scripts/logs.sh [service_name]

# Clean up everything (⚠️ deletes all data)
./scripts/clean.sh
```

## ⚙️ Configuration

### Environment Variables

Copy `.env.example` to `.env` and customize:

```bash
# Docker Compose Project
COMPOSE_PROJECT_NAME=dataeng-workshop

# MySQL Configuration
MYSQL_ROOT_PASSWORD=rootpassword123
MYSQL_DATABASE=beer_db
MYSQL_USER=student
MYSQL_PASSWORD=student123

# MinIO S3 Configuration
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin123
```

### Default Credentials

**JupyterHub:**
- Admin: `admin` / `admin123`
- Students can self-register

**MySQL:**
- User: `student` / `student123`
- Root: `root` / `rootpassword123`

**MinIO:**
- Access Key: `minioadmin`
- Secret Key: `minioadmin123`

## 🎓 For Instructors

### Deployment on University Server

1. **Copy repository to server**:
```bash
scp -r ul-m2-miage user@server:/path/to/workshop
```

2. **SSH into server and setup**:
```bash
ssh user@server
cd /path/to/workshop
./scripts/setup.sh
./scripts/start.sh
```

3. **Configure firewall** (if needed):
```bash
# Allow JupyterHub port
sudo ufw allow 8000/tcp
```

4. **Share access with students**:
   - URL: `http://server-ip:8000`
   - Instructions for self-registration
   - Workshop notebooks are pre-loaded

### Adding Students

Students can self-register through JupyterHub's web interface. To manually create accounts:

```bash
docker-compose exec jupyterhub bash
jupyterhub token --user=student1 --output=/tmp/token.txt
```

### Monitoring

```bash
# Check service status
./scripts/status.sh

# View resource usage
docker stats

# Check logs
./scripts/logs.sh jupyterhub
```

## 🔍 Troubleshooting

### Services won't start

```bash
# Check Docker is running
docker ps

# Check ports are not in use
netstat -tulpn | grep -E '(8000|3306|6379)'

# View detailed logs
docker-compose logs
```

### MySQL connection issues

```bash
# Verify MySQL is healthy
docker-compose exec mysql mysqladmin ping -p

# Check if data is loaded
docker-compose exec mysql mysql -uroot -p${MYSQL_ROOT_PASSWORD} \
  -e "USE beer_db; SHOW TABLES;"
```

### Out of memory

```bash
# Check resource usage
docker stats

# Reduce Spark worker memory in docker-compose.yml
# SPARK_WORKER_MEMORY=1G  (instead of 2G)
```

### Reset everything

```bash
./scripts/clean.sh  # ⚠️ Deletes all data
./scripts/setup.sh
./scripts/start.sh
```

## 📖 Learning Resources

### Connecting to Services from Python

All connection details are available as environment variables in notebooks:

```python
import os

# MySQL
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

# Redis
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')

# Spark
SPARK_MASTER = os.getenv('SPARK_MASTER')

# S3/MinIO
S3_ENDPOINT = os.getenv('S3_ENDPOINT')
S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')
```

### Example Queries

**MySQL:**
```sql
SELECT b.name, br.name as brewery, b.abv
FROM beers b
JOIN breweries br ON b.brewery_id = br.id
WHERE b.abv > 8
ORDER BY b.abv DESC;
```

**PySpark:**
```python
df = spark.read.csv('/opt/spark-data/csv/beers.csv', header=True)
df.filter(df.abv > 8).select('name', 'abv').show()
```

**Redis:**
```python
import redis
r = redis.Redis(host='redis', port=6379)
r.set('beer:1', 'Hocus Pocus')
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Students                              │
│                           ↓                                  │
│                   http://server:8000                         │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                      JupyterHub                              │
│              (Python Notebooks + Libraries)                  │
└─────────────────────────────────────────────────────────────┘
            ↓           ↓          ↓          ↓
    ┌───────────┐  ┌────────┐  ┌────────┐  ┌────────┐
    │   MySQL   │  │ Spark  │  │ Redis  │  │ Qdrant │
    │   8000+   │  │ Master │  │  KV    │  │ Vector │
    │   Beers   │  │   +2   │  │ Store  │  │   DB   │
    │           │  │Workers │  │        │  │        │
    └───────────┘  └────────┘  └────────┘  └────────┘
         ↓                                      ↓
    ┌─────────────────────────────────────────────┐
    │     MinIO S3 (Object Storage)               │
    │     - CSV files                             │
    │     - JSON files                            │
    │     - Backups                               │
    └─────────────────────────────────────────────┘
```

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional workshop notebooks
- More complex data pipelines
- Integration examples
- Performance optimizations

## 📝 License

This project is intended for educational purposes at University of Lorraine.

## 🔗 Additional Resources

- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [Qdrant Vector Database](https://qdrant.tech/documentation/)
- [Vespa Documentation](https://docs.vespa.ai/)
- [MinIO Documentation](https://min.io/docs/minio/linux/index.html)
- [JupyterHub Documentation](https://jupyterhub.readthedocs.io/)

## 📧 Support

For issues or questions:
1. Check the troubleshooting section
2. Review service logs: `./scripts/logs.sh [service]`
3. Contact the instructor

---

**Happy Data Engineering! 🚀🍺**

