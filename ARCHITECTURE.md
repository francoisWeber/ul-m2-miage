# Architecture Documentation

## System Overview

This document describes the architecture of the Data Engineering Workshop environment.

## Components

### 1. JupyterHub (Port 8000)
**Purpose:** Main entry point for students

**Technology Stack:**
- JupyterHub 4.0
- JupyterLab 4.0
- Python 3.11+
- Pre-installed libraries: PySpark, pandas, pymysql, redis, qdrant-client, boto3

**Features:**
- Multi-user support with authentication
- Isolated notebook environments per user
- Pre-configured connections to all data services
- Workshop notebooks included

**Resource Allocation:**
- CPU: Shared
- Memory: Based on host availability

### 2. MySQL (Port 3306)
**Purpose:** Relational database for structured data

**Data Schema:**
- `beers` - 8000+ records with beer information
- `breweries` - 1500+ brewery records
- `categories` - Beer categories
- `styles` - Beer styles
- `geocodes` - Geographic information

**Initialization:**
- SQL files automatically loaded from `beer-dataset/sql/`
- Foreign key relationships established
- Indexes created for performance

### 3. Apache Spark Cluster
**Purpose:** Distributed data processing

**Components:**
- Spark Master (Port 8080) - Cluster coordinator
- Spark Worker 1 (Port 8081) - 2 cores, 2GB RAM
- Spark Worker 2 (Port 8082) - 2 cores, 2GB RAM

**Access Methods:**
- PySpark from JupyterHub notebooks
- Spark SQL for SQL-like queries
- DataFrame API for data manipulation

**Data Access:**
- CSV files mounted at `/opt/spark-data/`
- Can connect to MySQL via JDBC
- Can read from S3/MinIO

### 4. Redis (Port 6379)
**Purpose:** In-memory key-value store

**Use Cases:**
- Caching frequently accessed data
- Session storage
- Real-time analytics
- Message queues (pub/sub)

**Persistence:**
- Append-only file (AOF) enabled
- Data persisted across restarts

### 5. Qdrant (Port 6333)
**Purpose:** Vector database for embeddings and semantic search

**Features:**
- Fast similarity search
- Multiple distance metrics (cosine, euclidean, dot product)
- REST and gRPC APIs
- Collections for organizing vectors

**Use Cases:**
- Semantic beer search
- Recommendation systems
- Clustering similar beers
- Embedding-based analytics

### 6. Vespa (Port 8088)
**Purpose:** Search engine and serving platform

**Features:**
- Full-text search
- Real-time indexing
- Machine learning model serving
- Rich query language

**Use Cases:**
- Beer catalog search
- Faceted search (by category, style, ABV)
- Ranking and relevance
- Real-time updates

### 7. MinIO (Ports 9000, 9001)
**Purpose:** S3-compatible object storage

**Features:**
- S3 API compatibility
- Web console for management
- Bucket policies and access control

**Contents:**
- `beer-dataset` bucket with all CSV files
- Automatically populated on startup
- Accessible via boto3 (AWS SDK)

### 8. Adminer (Port 8089)
**Purpose:** Database management UI

**Features:**
- Visual database browser
- Query editor with syntax highlighting
- Data import/export
- Schema visualization

## Network Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Docker Network                         │
│                 dataeng-network (bridge)                 │
│                                                          │
│  ┌──────────────┐                                       │
│  │  JupyterHub  │◄────────┐                            │
│  │  Port: 8000  │         │                            │
│  └───────┬──────┘         │                            │
│          │                │                            │
│          │  Connects to all services                   │
│          │                │                            │
│  ┌───────┼────────────────┼─────────────┐             │
│  │       ▼                ▼             │             │
│  │  ┌─────────┐     ┌──────────┐       │             │
│  │  │  MySQL  │     │  Redis   │       │             │
│  │  │  :3306  │     │  :6379   │       │             │
│  │  └─────────┘     └──────────┘       │             │
│  │                                       │             │
│  │  ┌─────────┐     ┌──────────┐       │             │
│  │  │ Qdrant  │     │  Vespa   │       │             │
│  │  │  :6333  │     │  :8080   │       │             │
│  │  └─────────┘     └──────────┘       │             │
│  │                                       │             │
│  │  ┌─────────────────────────────┐    │             │
│  │  │     Spark Cluster           │    │             │
│  │  │  Master + 2 Workers         │    │             │
│  │  │  :7077, :8080-8082          │    │             │
│  │  └─────────────────────────────┘    │             │
│  │                                       │             │
│  │  ┌─────────────────────────────┐    │             │
│  │  │     MinIO S3                │    │             │
│  │  │  API: 9000, Console: 9001   │    │             │
│  │  └─────────────────────────────┘    │             │
│  └───────────────────────────────────────┘           │
│                                                        │
└────────────────────────────────────────────────────────┘
         ▲                                    ▲
         │                                    │
    Host Ports                          Docker Volumes
  8000, 3306, etc.                   mysql_data, redis_data, etc.
```

## Data Flow

### 1. Student Access Flow
```
Student Browser → JupyterHub (8000) → Authentication → Notebook Spawn → Python Kernel
```

### 2. Data Query Flow
```
Notebook → Python Client Library → Service → Data Store → Response → Visualization
```

### 3. Spark Processing Flow
```
Notebook → PySpark → Spark Master → Distribute → Workers → Process → Aggregate → Return
```

### 4. Object Storage Flow
```
Notebook → boto3 → MinIO S3 → Bucket → Read/Write → Local/Spark
```

## Security Considerations

### Current Setup (Educational)
- Simple password authentication
- No SSL/TLS (HTTP only)
- Open signup enabled
- Shared network namespace
- Default passwords (should be changed)

### Production Recommendations
1. Use OAuth/LDAP for authentication
2. Enable SSL/TLS for all services
3. Implement role-based access control
4. Use secrets management (Vault, etc.)
5. Network segmentation
6. Regular backups
7. Monitoring and alerting

## Resource Requirements

### Minimum
- CPU: 4 cores
- RAM: 8GB
- Disk: 20GB

### Recommended
- CPU: 8+ cores
- RAM: 16GB+
- Disk: 50GB+ SSD

### Per-Service Allocation
| Service | CPU | Memory | Disk |
|---------|-----|--------|------|
| JupyterHub | 1-2 cores | 2GB | 5GB |
| MySQL | 1 core | 1GB | 10GB |
| Spark Master | 1 core | 1GB | 5GB |
| Spark Workers (x2) | 2 cores each | 2GB each | 5GB each |
| Redis | 0.5 core | 512MB | 1GB |
| Qdrant | 1 core | 1GB | 5GB |
| Vespa | 1 core | 2GB | 5GB |
| MinIO | 1 core | 512MB | 10GB |

## Scalability

### Horizontal Scaling
- Add more Spark workers: Edit docker-compose.yml
- Add JupyterHub spawner for multi-instance notebooks
- Replicate MySQL with read replicas
- Add Redis cluster nodes

### Vertical Scaling
- Increase worker memory: `SPARK_WORKER_MEMORY=4G`
- Increase worker cores: `SPARK_WORKER_CORES=4`
- Adjust MySQL buffer pool size
- Increase Redis maxmemory

## Monitoring

### Health Checks
- MySQL: `mysqladmin ping`
- Redis: `redis-cli ping`
- Spark: HTTP endpoint `/api/v1/applications`
- MinIO: `/minio/health/live`

### Metrics
- Docker stats: `docker stats`
- Spark UI: http://localhost:8080
- MinIO metrics: http://localhost:9001

### Logging
- Centralized: `docker-compose logs`
- Per-service: `docker-compose logs [service]`
- Log rotation configured in docker-compose

## Backup Strategy

### What to Backup
1. MySQL database (`mysql_data` volume)
2. MinIO buckets (`minio_data` volume)
3. JupyterHub user data (`jupyterhub_data` volume)
4. Configuration files (.env, docker-compose.yml)

### Backup Methods
```bash
# MySQL dump
docker-compose exec mysql mysqldump -u root -p beer_db > backup.sql

# MinIO bucket sync
mc mirror myminio/beer-dataset ./backup/

# Volume backup
docker run --rm -v mysql_data:/data -v $(pwd):/backup alpine tar czf /backup/mysql_backup.tar.gz /data
```

## Troubleshooting

### Common Issues

1. **Port conflicts**
   - Check: `netstat -tulpn | grep [port]`
   - Solution: Change port mappings in docker-compose.yml

2. **Out of memory**
   - Check: `docker stats`
   - Solution: Reduce Spark worker memory or add more RAM

3. **Slow performance**
   - Check resource usage
   - Verify SSD for Docker volumes
   - Increase worker count

4. **Connection timeouts**
   - Verify services are healthy: `./scripts/status.sh`
   - Check Docker network: `docker network inspect dataeng-network`
   - Review logs: `./scripts/logs.sh [service]`

## Future Enhancements

### Planned Features
- [ ] Kafka for streaming data
- [ ] Airflow for workflow orchestration
- [ ] Grafana + Prometheus for monitoring
- [ ] Elasticsearch for log aggregation
- [ ] Neo4j for graph analytics
- [ ] Superset for BI dashboards

### Integration Ideas
- Real-time beer rating updates
- Recommendation engine using Qdrant
- Geographic analysis with PostGIS
- Time-series analysis with InfluxDB

## References

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [JupyterHub Documentation](https://jupyterhub.readthedocs.io/)
- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)

