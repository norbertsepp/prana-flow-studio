python build.pytemplates/index.html

## CI/CD Mastery with GitHub Actions: Prana Flow Yoga Studio

Topic: Continuous Integration & Continuous Deployment (CI/CD) with GitHub Actions

Target Level: Practical proficiency in workflow orchestration, automated quality gates, artifact management, and automated GitHub Pages deployment

Structure: 5 Chapters (8–10 minutes per chapter)

## Course Outline & Setup

### Course Outline

1. **Chapter 1: The Studio Foundation & Build Engine** — Project layout, operational data schema (rooms, schedules, maintenance), and a Python/Jinja2 static generator.
2. **Chapter 2: Code Quality & CI Safety Nets** — Linting and formatting with Ruff, plus automated domain validations using Pytest (detecting maintenance conflicts and room capacity limits).
3. **Chapter 3: Workflow Anatomy & Automated Quality Gates** — YAML anatomy (events, jobs, steps, runners) and orchestrating Ruff and Pytest on push and pull requests.
4. **Chapter 4: Artifact Compilation in the Cloud** — Running the Python generator inside the runner virtual environment and publishing build artifacts.
5. **Chapter 5: Continuous Deployment to GitHub Pages** — Environment permissions, zero-downtime deployment actions, and testing a live maintenance update rollout.

### Exercise Environment & Setup Instructions

#### Prerequisites

* Python 3.10+ installed locally.
* Git installed and configured.
* A GitHub account with a new, empty public repository named `prana-flow-studio`.

#### Local Directory & Virtual Environment Setup

Run the following commands in your terminal:

```Shell
bash

mkdir prana-flow-studio
cd prana-flow-studio
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate  

# Install required tooling
pip install jinja2 pytest ruff
```

Save your dependencies:

```Shell
pip freeze > requirements.txt
```

Initialize your Git repository:

```Shell
Bash
git init
git branch -M main
```

Create a `.gitignore` file:

```Shell
Code snippet
.venv/
__pycache__/
.pytest_cache/
.ruff_cache/
_site/
*.pyc
```

## Chapter 1: The Studio Foundation & Build Engine

1. ### Theoretical Introduction

   At the core of automated CI/CD pipelines is a deterministic build step: taking raw structured data or source templates and compiling them into distribution-ready assets.

In modern static site generation (SSG) architectures, business data is maintained in clean formats like JSON or YAML. A build script parses that state, renders templates, and outputs flat static assets (`.html`, `.css`) into a target directory (often ` _site` or `dist`). Because static assets require no server-side execution runtime, they provide low-latency delivery, zero attack surface for code injection, and direct hosting on platforms like GitHub Pages.

```Shell
data/studio.json  ──┐
                    ├──> [ build.py (Jinja2) ] ──> _site/index.html
templates/page.html ┘
```

2. ## Steps to Complete the Chapter

   Define the data store (data/studio.json) containing room inventory, operational statuses (active, maintenance), classes, and instructors.

Build an HTML dashboard template using Jinja2 syntax.

Write build.py to process the JSON data, inject it into the template, and write the output to _site/index.html.

Run build.py locally and verify the resulting output in your browser.

3. ### General Exercises

   Inspect how Jinja2 renders loops:

```Python
from jinja2 import Template

template = Template("Rooms: {% for r in rooms %}{{ r }}, {% endfor %}")
print(template.render(rooms=["Studio A", "Studio B"]))
```

Practice creating directories programmatically in Python using

```Python
pathlib.Path("path/to/dir").mkdir(parents=True, exist_ok=True)
```

4. ### Case-Specific Tasks

   Task 1.1: Create data/studio.json containing at least two rooms (one active, one maintenance), instructors, and scheduled classes mapped to specific rooms.

   Task 1.2: Create templates/index.html with basic CSS and Jinja2 conditionals displaying a clear alert badge if a room is under maintenance.

   Task 1.3: Create build.py which reads data/studio.json, compiles templates/index.html, and produces _site/index.html.

   Task 1.4: Execute the script and verify that _site/index.html renders room statuses correctly.
5. ### Solutions

   data/studio.json

```JSON
{
  "studio_name": "Prana Flow Yoga Studio",
  "rooms": [
    {
      "id": "lotus-room",
      "name": "Lotus Room",
      "capacity": 25,
      "status": "active"
    },
    {
      "id": "shanti-hall",
      "name": "Shanti Hall",
      "capacity": 40,
      "status": "maintenance"
    }
  ],
  "instructors": [
    {"id": "maya", "name": "Maya Lin", "specialty": "Vinyasa Flow"},
    {"id": "arun", "name": "Arun Patel", "specialty": "Ashtanga"}
  ],
  "schedule": [
    {
      "id": "class-101",
      "title": "Sunrise Vinyasa",
      "room_id": "lotus-room",
      "instructor_id": "maya",
      "time": "07:00 AM",
      "registered": 18
    },
    {
      "id": "class-102",
      "title": "Pranayama & Meditation",
      "room_id": "lotus-room",
      "instructor_id": "arun",
      "time": "09:00 AM",
      "registered": 12
    }
  ]
}
```

```HTML
templates/index.html

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ studio_name }} - Daily Operations</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 2rem; background: #fdfbf7; color: #2d3748; }
    h1 { color: #2c5282; margin-bottom: 0.5rem; }
    .grid { display: grid; grid-template-columns: 1fr 2fr; gap: 2rem; margin-top: 1.5rem; }
    .card { background: white; padding: 1.25rem; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    .badge { display: inline-block; padding: 0.25rem 0.6rem; border-radius: 9999px; font-size: 0.75rem; font-weight: bold; text-transform: uppercase; }
    .badge-active { background: #c6f6d5; color: #22543d; }
    .badge-maintenance { background: #fed7d7; color: #742a2a; }
    table { width: 100%; border-collapse: collapse; margin-top: 0.5rem; }
    th, td { text-align: left; padding: 0.75rem; border-bottom: 1px solid #e2e8f0; }
  </style>
</head>
<body>
  <h1>{{ studio_name }}</h1>
  <p>Live Studio Schedule & Operational Room Status</p>

  <div class="grid">
    <div class="card">
      <h2>Rooms</h2>
      <ul>
        {% for room in rooms %}
          <li>
            <strong>{{ room.name }}</strong> (Max: {{ room.capacity }}) - 
            <span class="badge badge-{{ room.status }}">{{ room.status }}</span>
          </li>
        {% endfor %}
      </ul>
    </div>

    <div class="card">
      <h2>Today's Schedule</h2>
      <table>
        <thead>
          <tr>
            <th>Time</th>
            <th>Class</th>
            <th>Room</th>
            <th>Bookings</th>
          </tr>
        </thead>
        <tbody>
          {% for session in schedule %}
            <tr>
              <td>{{ session.time }}</td>
              <td><strong>{{ session.title }}</strong></td>
              <td>{{ session.room_name }}</td>
              <td>{{ session.registered }} attendees</td>
            </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </div>
</body>
</html>
```

build.py

```Python
import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def build_site():
    base_dir = Path(__file__).resolve().parent
    data_file = base_dir / "data" / "studio.json"
    template_dir = base_dir / "templates"
    output_dir = base_dir / "_site"

    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Denormalize room name into schedule for simple rendering
    room_map = {r["id"]: r["name"] for r in data["rooms"]}
    for session in data["schedule"]:
        session["room_name"] = room_map.get(session["room_id"], "Unknown Room")

    env = Environment(loader=FileSystemLoader(template_dir), autoescape=True)
    template = env.get_template("index.html")
    rendered_html = template.render(data)

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "index.html").write_text(rendered_html, encoding="utf-8")
    print("Site generated successfully at _site/index.html")


if __name__ == "__main__":
    build_site()
```

run and verify:

```Shell
python build.py
```

# Chapter 2: Code Quality & CI Safety Nets

## 1. Theoretical Introduction

Continuous Integration (CI) operates on a fundamental contract: bad code or invalid state must never merge into the main branch or reach production.

To enforce this, pipelines implement two layers of automated gates:

```bash
[ Git Push ] ──> [ Linter / Formatter Gate (Ruff) ] ──> [ Test Suite Gate (Pytest) ] ──> Pass/Fail
```

* **Static Analysis & Linting (Ruff)**: Fast, AST-level analysis written in Rust that detects syntax bugs, unused imports, anti-patterns, and style violations across codebases.
*  **Domain Invariant Testing (Pytest)**: Tests that validate business rules and data models rather than code mechanics.
  In our yoga studio, if an administrator marks a room as `status: "maintenance"` while classes are scheduled in it, the build must fail immediately with actionable feedback.


## 2. Steps to Complete the Chapter

* Configure Ruff in `pyproject.toml` to establish rule sets and format parameters.
* Execute Ruff checks and auto-formatting against the local codebase.
* Construct a validation module` tests/test_studio.py` containing domain assertion rules for the studio.
* Run `pytest` locally to confirm test outcomes.

## 3. General Exercises

1. Test Ruff's linter on any python script:

```Bash
ruff check .
```

2. Run Ruff format check without modifying files:

```Shell
ruff format --check .
```

3. Run Pytest with concise output:

```Shell
pytest -v
```


## 4. Case-Specific Tasks


* **Task 2.1**: Create` pyproject.toml` in your project root with Ruff configuration enabling core (`E, F`), bugbear (`B`), and import sorting (`I`).
* **Task 2.2:** Write `tests/test_studio.py` verifying two critical business rules:

  * No class can be assigned to a room currently set to ` maintenance`.
  * Registered attendees for a class cannot exceed the room's maximum capacity.
* **Task 2.3**: Run `ruff check .` and `ruff format .` to format all code.
* **Task 2.4**: Run `pytes` to confirm all validation checks pass.

## 5. Solutions

```TOML
pyproject.toml

Ini, TOML
[tool.ruff]
line-length = 88
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I", "B"]
ignore = []

[tool.pytest.ini_options]
testpaths = ["tests"]
```


tests/test_studio.py

```Python
import json
from pathlib import Path
import pytest


@pytest.fixture
def studio_data():
    data_path = Path(__file__).resolve().parent.parent / "data" / "studio.json"
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_no_classes_in_maintenance_rooms(studio_data):
    """Ensure no classes are scheduled in rooms under maintenance."""
    room_status = {r["id"]: r["status"] for r in studio_data["rooms"]}

    for session in studio_data["schedule"]:
        assigned_room = session["room_id"]
        status = room_status.get(assigned_room)
        assert status != "maintenance", (
            f"Business rule violation: Class '{session['title']}' is scheduled "
            f"in room '{assigned_room}' which is currently under maintenance!"
        )


def test_class_capacity_not_exceeded(studio_data):
    """Ensure session attendees do not exceed room capacity limits."""
    room_capacity = {r["id"]: r["capacity"] for r in studio_data["rooms"]}

    for session in studio_data["schedule"]:
        capacity = room_capacity.get(session["room_id"], 0)
        assert session["registered"] <= capacity, (
            f"Overcapacity: Class '{session['title']}' has {session['registered']} "
            f"attendees for a room capacity of {capacity}."
        )
```

Run checks:

```Shell
ruff check .
ruff format --check .
pytest -v
```

All tests should pass.
