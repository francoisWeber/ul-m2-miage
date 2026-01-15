#!/usr/bin/env python3
"""
Spark Load Test Launcher
Launches N parallel instances of the student simulation script
to test Spark cluster under load.
"""

import os
import sys
import time
import subprocess
import argparse
import signal
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

def log(message):
    """Print timestamped log message"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [LAUNCHER] {message}", flush=True)

def run_student(student_id, script_path, env_vars):
    """Run a single student simulation"""
    env = os.environ.copy()
    env.update(env_vars)
    env['STUDENT_ID'] = f'student-{student_id:03d}'
    
    start_time = time.time()
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            env=env,
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout per student
        )
        duration = time.time() - start_time
        
        return {
            'student_id': student_id,
            'success': result.returncode == 0,
            'duration': duration,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    except subprocess.TimeoutExpired:
        duration = time.time() - start_time
        return {
            'student_id': student_id,
            'success': False,
            'duration': duration,
            'stdout': '',
            'stderr': 'Timeout after 10 minutes',
            'returncode': -1
        }
    except Exception as e:
        duration = time.time() - start_time
        return {
            'student_id': student_id,
            'success': False,
            'duration': duration,
            'stdout': '',
            'stderr': str(e),
            'returncode': -1
        }

def main():
    parser = argparse.ArgumentParser(
        description='Launch parallel Spark student simulations for load testing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run 12 students in parallel
  python load_test_launcher.py --students 12
  
  # Run 5 students with staggered start (1 second delay)
  python load_test_launcher.py --students 5 --stagger 1
  
  # Run with custom Spark master
  SPARK_MASTER=spark://custom:7077 python load_test_launcher.py --students 10
        """
    )
    
    parser.add_argument(
        '--students', '-n',
        type=int,
        default=12,
        help='Number of students to simulate (default: 12)'
    )
    
    parser.add_argument(
        '--stagger', '-s',
        type=float,
        default=0.0,
        help='Delay in seconds between starting each student (default: 0)'
    )
    
    parser.add_argument(
        '--script', '-f',
        type=str,
        default=os.path.join(os.path.dirname(__file__), 'load_test_student.py'),
        help='Path to student simulation script (default: load_test_student.py)'
    )
    
    parser.add_argument(
        '--max-workers', '-w',
        type=int,
        default=None,
        help='Maximum number of parallel workers (default: same as --students)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show output from each student simulation'
    )
    
    args = parser.parse_args()
    
    # Validate script exists
    if not os.path.exists(args.script):
        log(f"ERROR: Script not found: {args.script}")
        return 1
    
    # Prepare environment variables
    env_vars = {
        'SPARK_MASTER': os.getenv('SPARK_MASTER', 'spark://spark-master:7077'),
    }
    
    log("=" * 70)
    log(f"Spark Load Test Launcher")
    log("=" * 70)
    log(f"Students to simulate: {args.students}")
    log(f"Stagger delay: {args.stagger}s")
    log(f"Script: {args.script}")
    log(f"Spark Master: {env_vars['SPARK_MASTER']}")
    log("=" * 70)
    
    start_time = time.time()
    results = []
    max_workers = args.max_workers or args.students
    
    # Launch students
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {}
        
        for student_id in range(1, args.students + 1):
            # Stagger start if requested
            if args.stagger > 0 and student_id > 1:
                time.sleep(args.stagger)
            
            log(f"Launching student {student_id:03d}...")
            future = executor.submit(run_student, student_id, args.script, env_vars)
            futures[future] = student_id
        
        # Collect results as they complete
        completed = 0
        for future in as_completed(futures):
            student_id = futures[future]
            result = future.result()
            results.append(result)
            completed += 1
            
            status = "✓ SUCCESS" if result['success'] else "✗ FAILED"
            log(f"Student {student_id:03d} completed: {status} ({result['duration']:.1f}s)")
            
            if args.verbose:
                if result['stdout']:
                    print(f"\n--- Student {student_id:03d} STDOUT ---")
                    print(result['stdout'])
                if result['stderr']:
                    print(f"\n--- Student {student_id:03d} STDERR ---")
                    print(result['stderr'])
    
    total_duration = time.time() - start_time
    
    # Summary
    log("=" * 70)
    log("LOAD TEST SUMMARY")
    log("=" * 70)
    
    successful = sum(1 for r in results if r['success'])
    failed = len(results) - successful
    
    log(f"Total students: {len(results)}")
    log(f"Successful: {successful}")
    log(f"Failed: {failed}")
    log(f"Total duration: {total_duration:.1f}s")
    log(f"Average duration per student: {sum(r['duration'] for r in results) / len(results):.1f}s")
    
    if results:
        durations = [r['duration'] for r in results]
        log(f"Min duration: {min(durations):.1f}s")
        log(f"Max duration: {max(durations):.1f}s")
    
    log("=" * 70)
    
    # Show failures
    if failed > 0:
        log("\nFAILED STUDENTS:")
        for result in results:
            if not result['success']:
                log(f"  Student {result['student_id']:03d}: {result['stderr'][:100]}")
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        log("\nInterrupted by user")
        sys.exit(130)
