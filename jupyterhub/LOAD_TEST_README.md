# Spark Load Testing Scripts

This directory contains scripts to simulate multiple students using Spark simultaneously, allowing you to load test your Spark cluster configuration before workshops.

## Files

- **`load_test_student.py`**: Simulates a single student session performing various Spark operations
- **`load_test_launcher.py`**: Launches N parallel student simulations
- **`LOAD_TEST_README.md`**: This file

## Quick Start

### Basic Usage

```bash
# Run 12 students in parallel (simulating 12 students in a workshop)
python load_test_launcher.py --students 12

# Run with staggered start (1 second delay between each student)
python load_test_launcher.py --students 12 --stagger 1

# Run with verbose output (see each student's output)
python load_test_launcher.py --students 12 --verbose
```

### Running Inside Docker Container

If you're running this from inside the JupyterHub container:

```bash
# From inside the container
cd /srv/jupyterhub  # or wherever the scripts are mounted
python load_test_launcher.py --students 12
```

### Running from Host Machine

If you want to run from your host machine (assuming scripts are mounted):

```bash
# Execute inside the container
docker exec -it jupyterhub python /path/to/load_test_launcher.py --students 12
```

## What the Student Simulation Does

Each student simulation (`load_test_student.py`) performs:

1. **Creates a Spark session** with a unique random name
2. **Reads CSV files** (beers.csv, breweries.csv)
3. **Simple operations**: count, filter, show
4. **UDF operations**: custom functions on DataFrames
5. **Joins and aggregations**: joining tables, groupBy operations
6. **Caching**: caching DataFrames and using them multiple times
7. **Complex queries**: multiple filters, sorts, aggregations

Between each exercise, there's a **random delay** (1-5 seconds) to simulate:
- Thinking time
- Typing code
- Reading instructions
- Different student paces

## Configuration

### Environment Variables

- `SPARK_MASTER`: Spark master URL (default: `spark://spark-master:7077`)
- `STUDENT_ID`: Unique identifier for the student (auto-generated if not set)

### Spark Session Configuration

Each student session uses:
- 1 executor core
- 500MB executor memory
- 256MB driver memory
- 1 core max (via `spark.cores.max`)

This matches the configuration students should use in the workshop.

## Examples

### Example 1: Test with 12 Students

```bash
python load_test_launcher.py --students 12
```

Output:
```
[14:30:15] [LAUNCHER] Spark Load Test Launcher
[14:30:15] [LAUNCHER] ======================================================================
[14:30:15] [LAUNCHER] Students to simulate: 12
[14:30:15] [LAUNCHER] Stagger delay: 0.0s
[14:30:15] [LAUNCHER] Script: load_test_student.py
[14:30:15] [LAUNCHER] Spark Master: spark://spark-master:7077
[14:30:15] [LAUNCHER] ======================================================================
[14:30:15] [LAUNCHER] Launching student 001...
[14:30:15] [LAUNCHER] Launching student 002...
...
[14:35:42] [LAUNCHER] Student 001 completed: ✓ SUCCESS (45.2s)
[14:35:43] [LAUNCHER] Student 002 completed: ✓ SUCCESS (46.1s)
...
[14:35:50] [LAUNCHER] ======================================================================
[14:35:50] [LAUNCHER] LOAD TEST SUMMARY
[14:35:50] [LAUNCHER] ======================================================================
[14:35:50] [LAUNCHER] Total students: 12
[14:35:50] [LAUNCHER] Successful: 12
[14:35:50] [LAUNCHER] Failed: 0
[14:35:50] [LAUNCHER] Total duration: 45.8s
[14:35:50] [LAUNCHER] Average duration per student: 45.2s
```

### Example 2: Staggered Start

```bash
# Start students 2 seconds apart (more realistic)
python load_test_launcher.py --students 12 --stagger 2
```

### Example 3: Test with Different Spark Master

```bash
SPARK_MASTER=spark://custom-master:7077 python load_test_launcher.py --students 10
```

### Example 4: Run Single Student (for debugging)

```bash
python load_test_student.py
```

Or with custom student ID:

```bash
STUDENT_ID=test-student-001 python load_test_student.py
```

## Monitoring During Load Test

While the load test is running, you can monitor:

### 1. Spark Master UI
```bash
# Open in browser
http://localhost:8080
```

You should see multiple applications running simultaneously, each with a unique name like `student-001-abc123`.

### 2. Spark Worker UI
```bash
# Open in browser
http://localhost:8081
```

Check resource usage, running executors, etc.

### 3. System Resources

```bash
# Memory usage
free -h

# Docker container stats
docker stats spark-worker-1 spark-master

# Disk usage
docker exec spark-worker-1 df -h /tmp/spark-local
```

### 4. Application Logs

Each student simulation logs its progress:
```
[14:30:15] [student-001] Starting student simulation: student-001
[14:30:16] [student-001] Creating Spark session: student-001-a1b2c3d4
[14:30:17] [student-001] === Exercise 1: Reading CSV files ===
[14:30:18] [student-001] Read beers.csv: 5840 rows
...
```

## Troubleshooting

### Issue: "Could not find CSV files"

**Solution**: Make sure the data files are mounted correctly. The script tries multiple paths:
- `/data/csv/beers.csv`
- `/datasets/csv/beers.csv`
- `/opt/spark-data/csv/beers.csv`

Check which path your setup uses and update the script if needed.

### Issue: "Connection refused" or "Cannot connect to Spark master"

**Solution**: 
1. Verify Spark master is running: `docker ps | grep spark-master`
2. Check SPARK_MASTER environment variable
3. Verify network connectivity from container to Spark master

### Issue: "Out of memory" errors

**Solution**: 
1. Reduce number of students: `--students 6`
2. Check Docker memory limits in `docker-compose.yml`
3. Monitor memory usage: `docker stats`
4. Reduce executor memory in `load_test_student.py` if needed

### Issue: Students timing out

**Solution**: 
- Increase timeout in `load_test_launcher.py` (default: 600 seconds)
- Check if Spark cluster is overloaded
- Reduce number of concurrent students

## Customization

### Modify Student Behavior

Edit `load_test_student.py` to:
- Add more exercises
- Change delay ranges
- Modify Spark configurations
- Add different types of operations

### Modify Launch Behavior

Edit `load_test_launcher.py` to:
- Change default parameters
- Add more monitoring
- Customize output format
- Add result logging to file

## Tips for Load Testing

1. **Start small**: Test with 2-3 students first, then scale up
2. **Monitor resources**: Watch memory, CPU, and disk usage
3. **Check Spark UI**: Verify applications are distributed correctly
4. **Stagger starts**: Use `--stagger` to simulate realistic arrival times
5. **Run multiple times**: Test consistency of your configuration
6. **Monitor logs**: Check for errors or warnings

## Expected Behavior

With proper configuration, you should see:
- ✅ All students complete successfully
- ✅ Spark UI shows multiple applications running
- ✅ Memory usage stays within limits
- ✅ No "out of memory" errors
- ✅ Applications complete in reasonable time (30-60 seconds each)
- ✅ No disk space issues

If you see failures or resource exhaustion, adjust your Spark configuration accordingly.
