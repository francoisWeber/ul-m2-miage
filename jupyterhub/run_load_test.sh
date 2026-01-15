#!/bin/bash
# Simple wrapper script to run Spark load tests

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAUNCHER_SCRIPT="${SCRIPT_DIR}/load_test_launcher.py"

# Default values
STUDENTS=12
STAGGER=0
VERBOSE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -n|--students)
            STUDENTS="$2"
            shift 2
            ;;
        -s|--stagger)
            STAGGER="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE="--verbose"
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  -n, --students N    Number of students to simulate (default: 12)"
            echo "  -s, --stagger SEC    Delay between starting each student (default: 0)"
            echo "  -v, --verbose       Show output from each student"
            echo "  -h, --help          Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0 --students 12"
            echo "  $0 --students 12 --stagger 2"
            echo "  $0 --students 12 --verbose"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 not found"
    exit 1
fi

# Check if launcher script exists
if [ ! -f "$LAUNCHER_SCRIPT" ]; then
    echo "Error: Launcher script not found: $LAUNCHER_SCRIPT"
    exit 1
fi

# Run the launcher
echo "Running Spark load test with $STUDENTS students..."
echo ""

python3 "$LAUNCHER_SCRIPT" \
    --students "$STUDENTS" \
    --stagger "$STAGGER" \
    $VERBOSE
