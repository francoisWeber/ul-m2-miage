import yaml

def extract_and_sum_resources(file_path):
    with open(file_path, 'r') as file:
        compose_data = yaml.safe_load(file)

    total_resources = {
        'cpus_limit': 0,
        'memory_limit': 0,
        'cpus_reservation': 0,
        'memory_reservation': 0
    }

    services = compose_data.get('services', {})

    for service_name, service in services.items():
        deploy = service.get('deploy', {})
        resources = deploy.get('resources', {})
        limits = resources.get('limits', {})
        reservations = resources.get('reservations', {})

        # Extract limits
        total_resources['cpus_limit'] += float(limits.get('cpus', 0))
        memory_limit = limits.get('memory', '0')
        total_resources['memory_limit'] += parse_memory(memory_limit)

        # Extract reservations
        total_resources['cpus_reservation'] += float(reservations.get('cpus', 0))
        memory_reservation = reservations.get('memory', '0')
        total_resources['memory_reservation'] += parse_memory(memory_reservation)

    return total_resources

def parse_memory(memory_str):
    """Convert memory strings like '512M', '1G' to numeric values in bytes."""
    if memory_str.endswith('G'):
        return float(memory_str[:-1]) * 1024 * 1024 * 1024
    elif memory_str.endswith('M'):
        return float(memory_str[:-1]) * 1024 * 1024
    elif memory_str.endswith('K'):
        return float(memory_str[:-1]) * 1024
    elif memory_str.endswith('B'):
        return float(memory_str[:-1])
    return float(memory_str)

if __name__ == "__main__":
    docker_compose_file = "docker-compose.yml"
    resources_totals = extract_and_sum_resources(docker_compose_file)

    print("Total Resources:")
    print(f"  CPU Limit: {int(resources_totals['cpus_limit'])}")
    print(f"  Memory Limit: {resources_totals['memory_limit'] / (1024 * 1024 * 1024):.2f} GB")
    print(f"  CPU Reservation: {int(resources_totals['cpus_reservation'])}")
    print(f"  Memory Reservation: {resources_totals['memory_reservation'] / (1024 * 1024 * 1024):.2f} GB")

