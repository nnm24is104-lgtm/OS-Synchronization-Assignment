
import threading
import time
import random
import json
import html

N = 4
ROUNDS = 2

forks = [threading.Semaphore(1) for _ in range(N)]
room = threading.Semaphore(N - 1)

states = ["Thinking"] * N
fork_owners = [None] * N
events = []
event_lock = threading.Lock()


def log_event(i, state, message):
    with event_lock:
        states[i] = state
        events.append({
            "time": round(time.time(), 3),
            "philosopher": i + 1,
            "state": state,
            "message": message,
            "states": states.copy(),
            "fork_owners": fork_owners.copy()
        })


def philosopher_work(i):
    left = i
    right = (i + 1) % N
    name = f"Philosopher {i + 1}"

    for r in range(1, ROUNDS + 1):
        log_event(i, "Thinking", f"{name} is thinking (round {r})")
        time.sleep(random.uniform(0.2, 0.5))

        log_event(i, "Hungry", f"{name} wants to eat")
        room.acquire()
        log_event(i, "Waiting for forks", f"{name} is waiting for forks")

        forks[left].acquire()
        with event_lock:
            fork_owners[left] = i + 1
            states[i] = "Acquiring Forks"
            events.append({
                "time": round(time.time(), 3),
                "philosopher": i + 1,
                "state": "Acquiring Forks",
                "message": f"{name} acquired Fork {left + 1}",
                "states": states.copy(),
                "fork_owners": fork_owners.copy()
            })

        forks[right].acquire()
        with event_lock:
            fork_owners[right] = i + 1
            states[i] = "Eating"
            events.append({
                "time": round(time.time(), 3),
                "philosopher": i + 1,
                "state": "Eating",
                "message": f"{name} acquired Fork {right + 1} and started eating",
                "states": states.copy(),
                "fork_owners": fork_owners.copy()
            })

        time.sleep(random.uniform(0.3, 0.6))

        with event_lock:
            states[i] = "Releasing Forks"
            fork_owners[right] = None
            events.append({
                "time": round(time.time(), 3),
                "philosopher": i + 1,
                "state": "Releasing Forks",
                "message": f"{name} released Fork {right + 1}",
                "states": states.copy(),
                "fork_owners": fork_owners.copy()
            })
        forks[right].release()

        with event_lock:
            fork_owners[left] = None
            events.append({
                "time": round(time.time(), 3),
                "philosopher": i + 1,
                "state": "Releasing Forks",
                "message": f"{name} released Fork {left + 1}",
                "states": states.copy(),
                "fork_owners": fork_owners.copy()
            })
        forks[left].release()
        room.release()

        log_event(i, "Thinking", f"{name} finished eating and is thinking again")

    log_event(i, "Finished", f"{name} completed both rounds")


def generate_html():
    trace = json.dumps(events).replace("</", "<\\/")
    page = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dining Philosophers - Semaphore</title>
<style>
body{font-family:Arial;background:#f2f5fa;color:#202b3c;margin:20px}
h1,h2{color:#203864}
.panel{background:white;padding:16px;margin:14px 0;border-radius:12px;box-shadow:0 2px 8px #0001}
.stage{position:relative;max-width:700px;height:440px;margin:auto}
.tabletop{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:220px;height:220px;border-radius:50%;background:#ead9ba;border:9px solid #9d7b52;display:flex;align-items:center;justify-content:center;text-align:center;font-weight:bold}
.person{position:absolute;transform:translate(-50%,-50%);width:130px;padding:10px 5px;text-align:center;border:2px solid #aab4c3;border-radius:12px;background:white;box-sizing:border-box}
.state{font-size:12px;margin-top:5px}
.eating{background:#d9f7e5;border-color:#198754}
.waiting{background:#fff0c2;border-color:#d59a21}
.finished{background:#e8edf3;border-color:#718096}
.fork{position:absolute;transform:translate(-50%,-50%);background:white;border:1px solid #8996a8;border-radius:20px;padding:7px;font-size:12px;white-space:nowrap}
.owned{background:#d7e8ff;border-color:#2670bd;font-weight:bold}
button{background:#203864;color:white;border:0;border-radius:6px;padding:9px 12px;margin:3px;cursor:pointer}
.controls{display:flex;gap:5px;align-items:center;flex-wrap:wrap}
input[type=range]{flex:1;min-width:150px}
table{border-collapse:collapse;width:100%;background:white;font-size:13px}
th,td{border:1px solid #d5dce6;padding:8px;text-align:left}
th{background:#203864;color:white}
tr:nth-child(even){background:#edf2f8}
.wrap{overflow-x:auto}
</style>
</head>
<body>
<h1>Dining Philosophers - Semaphore Solution</h1>
<div class="panel">
<p><b>Philosophers:</b> 4 | <b>Forks:</b> 4 | <b>Rounds:</b> 2 each</p>
<p><b>Deadlock prevention:</b> Room semaphore permits at most three philosophers to compete for forks.</p>
<p><b>Actual recorded events:</b> <span id="total"></span></p>
</div>
<div class="panel">
<h2>Execution Replay</h2>
<div class="stage">
<div class="tabletop">Dining<br>Table</div>
<div class="person" id="p0">Philosopher 1<div class="state"></div></div>
<div class="person" id="p1">Philosopher 2<div class="state"></div></div>
<div class="person" id="p2">Philosopher 3<div class="state"></div></div>
<div class="person" id="p3">Philosopher 4<div class="state"></div></div>
<div class="fork" id="f0">Fork 1</div><div class="fork" id="f1">Fork 2</div>
<div class="fork" id="f2">Fork 3</div><div class="fork" id="f3">Fork 4</div>
</div>
<div class="controls">
<button id="play">Play</button><button id="prev">Previous</button>
<button id="next">Next</button><input id="slider" type="range" min="0" value="0">
<span id="counter"></span>
</div>
<p id="message"></p>
</div>
<div class="panel">
<h2>Actual Execution Timeline</h2>
<div class="wrap"><table><thead><tr><th>#</th><th>Time</th><th>Philosopher</th><th>State</th><th>Event</th><th>Fork ownership</th></tr></thead><tbody id="rows"></tbody></table></div>
</div>
<script>
const events=__TRACE__;
document.getElementById("total").textContent=events.length;
const pp=[{x:50,y:9},{x:87,y:50},{x:50,y:91},{x:13,y:50}];
const fp=[{x:69,y:22},{x:79,y:68},{x:31,y:79},{x:21,y:32}];
pp.forEach((p,i)=>{let e=document.getElementById("p"+i);e.style.left=p.x+"%";e.style.top=p.y+"%";});
fp.forEach((p,i)=>{let e=document.getElementById("f"+i);e.style.left=p.x+"%";e.style.top=p.y+"%";});
const rows=document.getElementById("rows");
events.forEach((e,i)=>{let tr=document.createElement("tr");
let owner=e.fork_owners.map((v,j)=>"F"+(j+1)+": "+(v===null?"Free":"P"+v)).join(" | ");
[i+1,e.time,"P"+e.philosopher,e.state,e.message,owner].forEach(v=>{let td=document.createElement("td");td.textContent=v;tr.appendChild(td);});rows.appendChild(tr);});
let index=0,timer=null;
const slider=document.getElementById("slider");slider.max=Math.max(0,events.length-1);
function render(){
if(!events.length)return;
let e=events[index];
e.states.forEach((s,i)=>{let el=document.getElementById("p"+i);el.className="person";
if(s==="Eating")el.classList.add("eating");
if(s.includes("Waiting")||s==="Hungry"||s==="Acquiring Forks")el.classList.add("waiting");
if(s==="Finished")el.classList.add("finished");
el.querySelector(".state").textContent=s;});
e.fork_owners.forEach((o,i)=>{let el=document.getElementById("f"+i);el.classList.toggle("owned",o!==null);el.textContent="Fork "+(i+1)+": "+(o===null?"Free":"P"+o);});
document.getElementById("message").textContent="P"+e.philosopher+" — "+e.message;
document.getElementById("counter").textContent=(index+1)+" / "+events.length;slider.value=index;}
function stop(){if(timer){clearInterval(timer);timer=null;}document.getElementById("play").textContent="Play";}
document.getElementById("play").onclick=()=>{if(timer){stop();return;}if(index>=events.length-1)index=0;document.getElementById("play").textContent="Pause";timer=setInterval(()=>{if(index>=events.length-1){stop();return;}index++;render();},800);render();};
document.getElementById("prev").onclick=()=>{stop();index=Math.max(0,index-1);render();};
document.getElementById("next").onclick=()=>{stop();index=Math.min(events.length-1,index+1);render();};
slider.oninput=()=>{stop();index=Number(slider.value);render();};
render();
</script>
</body>
</html>"""
    page = page.replace("__TRACE__", trace)
    with open("dining_philosophers_semaphore.html", "w", encoding="utf-8") as f:
        f.write(page)


if __name__ == "__main__":
    threads = [threading.Thread(target=philosopher_work, args=(i,)) for i in range(N)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    with event_lock:
        assert all(owner is None for owner in fork_owners)
        assert all(state == "Finished" for state in states)
        trace = events.copy()

    with open("dining_philosophers_semaphore_events.json", "w", encoding="utf-8") as f:
        json.dump(trace, f, indent=2)

    generate_html()
    print("Semaphore execution completed.")
    print("Events recorded:", len(trace))
    print("All forks released: PASSED")
    print("Generated dining_philosophers_semaphore.html")
