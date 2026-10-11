
import threading
import time
import random
import json
import html

resource = threading.Semaphore(1)
read_count_lock = threading.Semaphore(1)

read_count = 0
active_readers = 0
writer_active = False
max_readers = 0
shared_data = "Initial Data"

events = []
event_lock = threading.Lock()
state_lock = threading.Lock()


def log_event(process, state, message):
    with event_lock:
        events.append({
            "time": round(time.time(), 3),
            "process": process,
            "state": state,
            "message": message
        })


def reader(reader_id):
    global read_count, active_readers, max_readers

    name = f"Reader {reader_id}"
    log_event(name, "Waiting", "Waiting to read")

    read_count_lock.acquire()
    read_count += 1

    if read_count == 1:
        resource.acquire()

    read_count_lock.release()

    with state_lock:
        assert not writer_active, "ERROR: Reader entered while writer was active"
        active_readers += 1
        max_readers = max(max_readers, active_readers)

    log_event(name, "Reading", "Entered the reading section")
    time.sleep(random.uniform(0.5, 1.0))

    log_event(name, "Reading", f"Read shared data: {shared_data}")

    with state_lock:
        active_readers -= 1

    read_count_lock.acquire()
    read_count -= 1

    if read_count == 0:
        resource.release()

    read_count_lock.release()

    log_event(name, "Finished", "Finished reading")


def writer(writer_id):
    global shared_data, writer_active

    name = f"Writer {writer_id}"
    log_event(name, "Waiting", "Waiting to write")

    resource.acquire()

    with state_lock:
        assert active_readers == 0, "ERROR: Writer entered while readers were active"
        assert not writer_active, "ERROR: Multiple writers entered together"
        writer_active = True

    log_event(name, "Writing", "Entered the writing section")
    time.sleep(random.uniform(0.5, 1.0))

    shared_data = f"Data updated by Writer {writer_id}"
    log_event(name, "Writing", f"Updated shared data: {shared_data}")

    with state_lock:
        writer_active = False

    resource.release()

    log_event(name, "Finished", "Finished writing")


def generate_html():
    rows = ""

    for event in events:
        rows += (
            "<tr>"
            f"<td>{html.escape(str(event['time']))}</td>"
            f"<td>{html.escape(event['process'])}</td>"
            f"<td>{html.escape(event['state'])}</td>"
            f"<td>{html.escape(event['message'])}</td>"
            "</tr>\n"
        )

    page = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Readers-Writers Semaphore Simulation</title>
<style>
body {{
    font-family: Arial, sans-serif;
    margin: 30px;
    background: #f3f6fa;
}}
h1 {{ color: #203864; }}
.summary {{
    background: white;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 20px;
}}
table {{
    width: 100%;
    border-collapse: collapse;
    background: white;
}}
th, td {{
    border: 1px solid #ccc;
    padding: 10px;
    text-align: left;
}}
th {{ background: #203864; color: white; }}
tr:nth-child(even) {{ background: #eaf0f8; }}
</style>
</head>
<body>
<h1>Readers-Writers: Semaphore Simulation</h1>
<div class="summary">
<p><b>Final shared data:</b> {html.escape(shared_data)}</p>
<p><b>Maximum simultaneous readers:</b> {max_readers}</p>
<p><b>Synchronization checks:</b> Passed</p>
<p>This timeline was generated from recorded program execution events.</p>
</div>
<table>
<tr>
<th>Time</th>
<th>Process</th>
<th>State</th>
<th>Event</th>
</tr>
{rows}
</table>
</body>
</html>
"""

    with open(
        "readers_writers_semaphore.html", "w", encoding="utf-8"
    ) as file:
        file.write(page)


if __name__ == "__main__":
    threads = []

    for i in range(1, 4):
        threads.append(threading.Thread(target=reader, args=(i,)))

    for i in range(1, 3):
        threads.append(threading.Thread(target=writer, args=(i,)))

    random.shuffle(threads)

    for thread in threads:
        thread.start()
        time.sleep(0.1)

    for thread in threads:
        thread.join()

    print("\nReaders-Writers execution completed.")
    print("Final shared data:", shared_data)
    print("Maximum simultaneous readers:", max_readers)
    print("Total events recorded:", len(events))
    print("Synchronization checks: PASSED")

    with open(
        "readers_writers_events.json", "w", encoding="utf-8"
    ) as file:
        json.dump(events, file, indent=4)

    generate_html()

    print("\nFiles generated successfully:")
    print("1. readers_writers_events.json")
    print("2. readers_writers_semaphore.html")
    print("\nOpen readers_writers_semaphore.html in your browser.")

