# OS-Synchronization-Assignment
Operating Systems synchronization assignment using semaphores, monitors, and HTML simulations.
# OS Synchronization Assignment

## Project Overview

This project implements synchronization algorithms for the Readers–Writers Problem and Dining Philosophers Problem using semaphores and monitors. Each implementation uses concurrent execution and provides HTML simulations based on recorded execution events.

## Objectives

- Implement synchronization algorithms using semaphores and monitors.
- Understand mutual exclusion and concurrent execution.
- Observe synchronization events through HTML simulations.
- Study race conditions, deadlock, and starvation.

## Technologies Used

- Python
- Threading and synchronization primitives
- HTML
- JSON

## Implementations

### 1. Readers–Writers Problem

- `readers_writers_semaphore.py` — Semaphore-based implementation.
- `readers_writers_monitor.py` — Monitor-based implementation.

### 2. Dining Philosophers Problem

- `dining_philosophers_semaphore.py` — Semaphore-based implementation with four philosophers.
- `dining_philosophers_monitor.py` — Monitor-based implementation with four philosophers.

## Repository Structure

| File | Description |
|---|---|
| `readers_writers_semaphore.py` | Readers–Writers using semaphores |
| `readers_writers_monitor.py` | Readers–Writers using monitors |
| `dining_philosophers_semaphore.py` | Dining Philosophers using semaphores |
| `dining_philosophers_monitor.py` | Dining Philosophers using monitors |
| `readers_writers_semaphore.html` | Semaphore-based Readers–Writers simulation |
| `readers_writers_monitor.html` | Monitor-based Readers–Writers simulation |
| `dining_philosophers_semaphore.html` | Semaphore-based Dining Philosophers simulation |
| `dining_philosophers_monitor.html` | Monitor-based Dining Philosophers simulation |
| `*_events.json` | Recorded synchronization events |

## Requirements

- Python 3
- A modern web browser

## How to Run

Open a terminal in the project directory and run each program separately.

```bash
python readers_writers_semaphore.py
python readers_writers_monitor.py
python dining_philosophers_semaphore.py
python dining_philosophers_monitor.py
```

Open the corresponding HTML files in a web browser to view the simulations.

## Expected Results

- Concurrent execution of readers and writers with synchronization.
- Four philosophers competing for forks while following synchronization rules.
- Recorded execution events in JSON files.
- HTML simulations visualizing synchronization activity.

## Conclusion

This project demonstrates how semaphores and monitors coordinate concurrent processes and threads. The implementations and HTML simulations help illustrate synchronization, mutual exclusion, and the challenges of concurrent execution.
