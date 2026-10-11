import threading
import time
import random
import json
import html

N = 4
ROUNDS = 2

states = ["Thinking"] * N
fork_owners = [None] * N
events = []
condition = threading.Condition()


def record_event(philosopher, state, message):
    events.append({
        "time": round(time.time(), 3),
        "philosopher": f"P{philosopher + 1}",
        "state": state,
        "event": message,
        "forks": [
            f"F{i + 1}: {'Free' if owner is None else 'P' + str(owner + 1)}"
            for i, owner in enumerate(fork_owners)
        ]
    })


def can_eat(i):
    left = (i - 1) % N
    right = (i + 1) % N
    return states[left] != "Eating" and states[right] != "Eating"


def pickup_forks(i):
    with condition:
        states[i] = "Hungry"
        record_event(i, "Hungry", f"Philosopher {i + 1} wants to eat")

        while not can_eat(i):
            record_event(
                i, "Waiting",
                f"Philosopher {i + 1} waits for neighboring philosophers"
            )
            condition.wait()

        states[i] = "Eating"
        left_fork = i
        right_fork = (i + 1) % N

        fork_owners[left_fork] = i
        fork_owners[right_fork] = i

        record_event(
            i, "Eating",
            f"Philosopher {i + 1} acquired both forks and started eating"
        )


def putdown_forks(i):
    with condition:
        states[i] = "Releasing"
        record_event(
            i, "Releasing",
            f"Philosopher {i + 1} is releasing both forks"
        )

        fork_owners[i] = None
        fork_owners[(i + 1) % N] = None

        states[i] = "Thinking"
        record_event(
            i, "Thinking",
            f"Philosopher {i + 1} finished eating and released both forks"
        )

        condition.notify_all()


def philosopher(i):
    for round_number in range(1, ROUNDS + 1):
        with condition:
            states[i] = "Thinking"
            record_event(
                i, "Thinking",
                f"Philosopher {i + 1} is thinking (round {round_number})"
            )

        time.sleep(random.uniform(0.1, 0.4))

        pickup_forks(i)
        time.sleep(random.uniform(0.2, 0.5))
        putdown_forks(i)

    with condition:
        states[i] = "Finished"
        record_event(
            i, "Finished",
            f"Philosopher {i + 1} completed both rounds"
        )
        condition.notify_all()


def generate_html():
    rows = ""

    for event in events:
        forks = " | ".join(event["forks"])

        rows += (
            "<tr>"
            f"<td>{event['time']}</td>"
            f"<td>{html.escape(event['philosopher'])}</td>"
            f"<td>{html.escape(event['state'])}</td>"
            f"<td>{html.escape(event['event'])}</td>"
            f"<td>{html.escape(forks)}</td>"
            "</tr>"
        )

    philosopher_summary = ""

    for i in range(N):
        philosopher_summary += (
            f"<li>Philosopher {i + 1}: "
            f"{html.escape(states[i])}</li>"
        )

    page = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Dining Philosophers - Monitor</title>
<style>
body {{
    font-family: Arial, sans-serif;
    margin: 25px;
    background: #f4f6f8;
}}
h1, h2 {{
    color: #243b53;
}}
.summary {{
    background: white;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 20px;
}}
.table-container {{
    overflow-x: auto;
    background: white;
}}
table {{
    border-collapse: collapse;
    width: 100%;
    font-size: 13px;
}}
th, td {{
    border: 1px solid #d5dce3;
    padding: 9px;
    text-align: left;
}}
th {{
    background: #243b53;
    color: white;
}}
tr:nth-child(even) {{
    background: #eef3f7;
}}
</style>
</head>
<body>
<h1>Dining Philosophers — Monitor Solution</h1>

<div class="summary">
<h2>Simulation Summary</h2>
<p><b>Philosophers:</b> {N}</p>
<p><b>Forks:</b> {N}</p>
<p><b>Synchronization:</b> Monitor using threading.Condition</p>
<p><b>Rounds per philosopher:</b> {ROUNDS}</p>
<p><b>Total events:</b> {len(events)}</p>

<h2>Final Philosopher States</h2>
<ul>{philosopher_summary}</ul>

<h2>Fork Ownership at Completion</h2>
<p>{' | '.join(
    f'F{i + 1}: {"Free" if owner is None else "P" + str(owner + 1)}'
    for i, owner in enumerate(fork_owners)
)}</p>
</div>

<h2>Actual Execution Timeline</h2>
<p>Fork ownership is recorded at each event. Free means the fork is available.</p>

<div class="table-container">
<table>
<thead>
<tr>
<th>Time</th>
<th>Philosopher</th>
<th>State</th>
<th>Event</th>
<th>Fork Ownership</th>
</tr>
</thead>
<tbody>
{rows}
</tbody>
</table>
</div>
</body>
</html>
"""

    with open("dining_philosophers_monitor.html", "w", encoding="utf-8") as file:
        file.write(page)


def main():
    threads = []

    for i in range(N):
        thread = threading.Thread(target=philosopher, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    with condition:
        assert all(owner is None for owner in fork_owners)
        assert all(state == "Finished" for state in states)

        eating_events = [
            event for event in events if event["state"] == "Eating"
        ]

        assert len(eating_events) == N * ROUNDS

        print("Dining Philosophers Monitor execution completed.")
        print("Number of philosophers:", N)
        print("Eating rounds per philosopher:", ROUNDS)
        print("Total events recorded:", len(events))
        print("All forks released: PASSED")
        print("Synchronization checks: PASSED")

        with open(
            "dining_philosophers_monitor_events.json",
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(events, file, indent=4)

    generate_html()

    print("\nFiles generated successfully:")
    print("1. dining_philosophers_monitor_events.json")
    print("2. dining_philosophers_monitor.html")
    print("\nOpen dining_philosophers_monitor.html in your browser.")


if __name__ == "__main__":
    main()
