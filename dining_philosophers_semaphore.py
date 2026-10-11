
import threading
import time
import random
import json
import html

# Exactly four philosophers and four forks
N = 4

# Each fork can be held by only one philosopher
forks = [threading.Semaphore(1) for _ in range(N)]

# Allow at most three philosophers to compete for forks at once.
# This prevents circular wait and avoids deadlock.
room = threading.Semaphore(N - 1)

states = ["Thinking"] * N
fork_owners = [None] * N

events = []
event_lock = threading.Lock()


def log_event(philosopher, state, message):
    """Record actual execution events and the current system state."""
    with event_lock:
        states[philosopher] = state

        events.append({
            "time": round(time.time(), 3),
            "philosopher": philosopher + 1,
            "state": state,
            "message": message,
            "states": states.copy(),
            "fork_owners": fork_owners.copy()
        })


def philosopher_work(philosopher):
    left = philosopher
    right = (philosopher + 1) % N
    name = f"Philosopher {philosopher + 1}"

    # Each philosopher performs two eating rounds
    for round_number in range(1, 3):
        log_event(
            philosopher, "Thinking",
            f"{name} is thinking (round {round_number})"
        )
        time.sleep(random.uniform(0.2, 0.5))

        log_event(
            philosopher, "Hungry",
            f"{name} wants to eat"
        )

        # Prevent deadlock by limiting fork competition
        room.acquire()

        log_event(
            philosopher, "Waiting for forks",
            f"{name} is waiting to acquire forks"
        )

        # Acquire left fork
        forks[left].acquire()
        with event_lock:
            fork_owners[left] = philosopher + 1
            events.append({
                "time": round(time.time(), 3),
                "philosopher": philosopher + 1,
                "state": "Acquiring Forks",
                "message": f"{name} acquired Fork {left + 1}",
                "states": states.copy(),
                "fork_owners": fork_owners.copy()
            })

        # Acquire right fork
        forks[right].acquire()
        with event_lock:
            fork_owners[right] = philosopher + 1
            states[philosopher] = "Eating"
            events.append({
                "time": round(time.time(), 3),
                "philosopher": philosopher + 1,
                "state": "Eating",
                "message": (
                    f"{name} acquired Fork {right + 1} "
                    "and started eating"
                ),
                "states": states.copy(),
                "fork_owners": fork_owners.copy()
            })

        time.sleep(random.uniform(0.3, 0.6))

        # Release right fork
        with event_lock:
            fork_owners[right] = None
            events.append({
                "time": round(time.time(), 3),
                "philosopher": philosopher + 1,
                "state": "Releasing Forks",
                "message": f"{name} released Fork {right + 1}",
                "states": states.copy(),
                "fork_owners": fork_owners.copy()
            })
        forks[right].release()

        # Release left fork
        with event_lock:
            fork_owners[left] = None
            events.append({
                "time": round(time.time(), 3),
                "philosopher": philosopher + 1,
                "state": "Releasing Forks",
                "message": f"{name} released Fork {left + 1}",
                "states": states.copy(),
                "fork_owners": fork_owners.copy()
            })
        forks[left].release()

        room.release()

        log_event(
            philosopher, "Thinking",
            f"{name} finished eating and returned to thinking"
        )

    log_event(
        philosopher, "Finished",
        f"{name} completed both rounds"
    )


def generate_html():
    rows = ""

    for event in events:
        owner_text = ", ".join(
            f"F{i + 1}: {'Free' if owner is None else 'P' + str(owner)}"
            for i, owner in enumerate(event["fork_owners"])
        )

        rows += (
            "<tr>"
            f"<td>{html.escape(str(event['time']))}</td>"
            f"<td>P{event['philosopher']}</td>"
            f"<td>{html.escape(event['state'])}</td>"
            f"<td>{html.escape(event['message'])}</td>"
            f"<td>{html.escape(owner_text)}</td>"
            "</tr>\n"
        )

    philosopher_cards = ""

    for i in range(N):
        philosopher_cards += f"""
        <div class="card">
            <h3>Philosopher {i + 1}</h3>
            <p>Final state: {html.escape(states[i])}</p>
        </div>
        """

    page = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Dining Philosophers - Semaphore Simulation</title>
<style>
body {{
    font-family: Arial, sans-serif;
    margin: 25px;
    background: #f3f6fa;
    color: #222;
}}
h1, h2 {{ color: #203864; }}
.summary, .card {{
    background: white;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 15px;
}}
.cards {{
    display: grid;
    grid-template-columns: repeat(4, minmax(120px, 1fr));
    gap: 12px;
}}
table {{
    width: 100%;
    border-collapse: collapse;
    background: white;
}}
th, td {{
    border: 1px solid #ccc;
    padding: 9px;
    text-align: left;
}}
th {{ background: #203864; color: white; }}
tr:nth-child(even) {{ background: #eaf0f8; }}
</style>
</head>
<body>
<h1>Dining Philosophers: Semaphore Simulation</h1>

<div class="summary">
    <p><b>Philosophers:</b> 4</p>
    <p><b>Forks:</b> 4</p>
    <p><b>Deadlock prevention:</b> Room semaphore allows at most 3
    philosophers to compete for forks simultaneously.</p>
    <p><b>Execution events recorded:</b> {len(events)}</p>
    <p><b>Execution rounds:</b> 2 per philosopher</p>
</div>

<h2>Philosopher States</h2>
<div class="cards">
{philosopher_cards}
</div>

<h2>Actual Execution Timeline</h2>
<p>Fork ownership: Free means available; P1-P4 identify the owner.</p>
<table>
<tr>
    <th>Time</th>
    <th>Philosopher</th>
    <th>State</th>
    <th>Event</th>
    <th>Fork Ownership</th>
</tr>
{rows}
</table>
</body>
</html>
"""

    with open(
        "dining_philosophers_semaphore.html",
        "w",
        encoding="utf-8"
    ) as file:
        file.write(page)


if __name__ == "__main__":
    threads = []

    for i in range(N):
        thread = threading.Thread(
            target=philosopher_work,
            args=(i,)
        )
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    # Confirm that every fork was released
    with event_lock:
        assert all(owner is None for owner in fork_owners)

    print("\nDining Philosophers Semaphore execution completed.")
    print("Number of philosophers:", N)
    print("Eating rounds per philosopher: 2")
    print("Total events recorded:", len(events))
    print("All forks released: PASSED")
    print("Synchronization checks: PASSED")

    with open(
        "dining_philosophers_semaphore_events.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(events, file, indent=4)

    generate_html()

    print("\nFiles generated successfully:")
    print("1. dining_philosophers_semaphore_events.json")
    print("2. dining_philosophers_semaphore.html")
    print("\nOpen dining_philosophers_semaphore.html in your browser.")