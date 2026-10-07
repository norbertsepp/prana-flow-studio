name: CI/CD Pipeline - Prana Flow Studio

on:
  push:
    branches: [ "main" ]
  workflow_dispatch:

# Permissions required for GitHub Pages deployment

permissions:
  contents: read
  pages: write
  id-token: write

# Allow only one concurrent deployment, skipping runs queued between the run in-progress and latest

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install ruff pytest jinja2

      - name: Run Ruff Linter
        run: ruff check .

      - name: Check Code Formatting
        run: ruff format --check .

      - name: Run Domain Validation Tests
        run: pytest -v

  build:
    needs: lint-and-test
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install build dependencies
        run: |
          python -m pip install --upgrade pip
          pip install jinja2

      - name: Build static site
        run: python build.py

      - name: Upload Pages artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: "_site"

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4

# CI/CD Mastery with GitHub Actions: Prana Flow Yoga Studio

Topic: Continuous Integration & Continuous Deployment (CI/CD) with GitHub Actions

Target Level: Practical proficiency in workflow orchestration, automated quality gates, artifact management, and automated GitHub Pages deployment

Structure: 5 Chapters (8–10 minutes per chapter)

# Course Outline & Setup

## Course Outline

1. **Chapter 1: The Studio Foundation & Build Engine** — Project layout, operational data schema (rooms, schedules, maintenance), and a Python/Jinja2 static generator.
2. **Chapter 2: Code Quality & CI Safety Nets** — Linting and formatting with Ruff, plus automated domain validations using Pytest (detecting maintenance conflicts and room capacity limits).
3. **Chapter 3: Workflow Anatomy & Automated Quality Gates** — YAML anatomy (events, jobs, steps, runners) and orchestrating Ruff and Pytest on push and pull requests.
4. **Chapter 4: Artifact Compilation in the Cloud** — Running the Python generator inside the runner virtual environment and publishing build artifacts.
5. **Chapter 5: Continuous Deployment to GitHub Pages** — Environment permissions, zero-downtime deployment actions, and testing a live maintenance update rollout.

## Exercise Environment & Setup Instructions

### Prerequisites

* Python 3.10+ installed locally.
* Git installed and configured.
* A GitHub account with a new, empty public repository named `prana-flow-studio`.

### Local Directory & Virtual Environment Setup

Run the following commands in your terminal:

```Shell
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
git init
git branch -M main
```

Create a `.gitignore` file:

```Shell
.venv/
__pycache__/
.pytest_cache/
.ruff_cache/
_site/
*.pyc
```

# Chapter 1: The Studio Foundation & Build Engine

## 1.1. Theoretical Introduction

  At the core of automated CI/CD pipelines is a deterministic build step: taking raw structured data or source templates and compiling them into distribution-ready assets.

In modern static site generation (SSG) architectures, business data is maintained in clean formats like JSON or YAML. A build script parses that state, renders templates, and outputs flat static assets (`.html`, `.css`) into a target directory (often `_site` or `dist`). Because static assets require no server-side execution runtime, they provide low-latency delivery, zero attack surface for code injection, and direct hosting on platforms like GitHub Pages.

```Shell
data/studio.json  ──┐
                    ├──> [ build.py (Jinja2) ] ──> _site/index.html
templates/page.html ┘
```

## 1.2. Steps to Complete the Chapter

* Define the data store (data/studio.json) containing room inventory, operational statuses (active, maintenance), classes, and instructors.
* Build an HTML dashboard template using Jinja2 syntax.
* Write build.py to process the JSON data, inject it into the template, and write the output to _site/index.html.
* Run build.py locally and verify the resulting output in your browser.

## 1.3. General Exercises

* Inspect how Jinja2 renders loops:

```Python
from jinja2 import Template

template = Template("Rooms: {% for r in rooms %}{{ r }}, {% endfor %}")
print(template.render(rooms=["Studio A", "Studio B"]))
```

* Practice creating directories programmatically in Python using

```Python
pathlib.Path("path/to/dir").mkdir(parents=True, exist_ok=True)
```

## 1.4. Case-Specific Tasks

* Task 1.4.1: Create data/studio.json containing at least two rooms (one active, one maintenance), instructors, and scheduled classes mapped to specific rooms.
* Task 1.4.2: Create templates/index.html with basic CSS and Jinja2 conditionals displaying a clear alert badge if a room is under maintenance.
* Task 1.4.3: Create build.py which reads data/studio.json, compiles templates/index.html, and produces _site/index.html.
* Task 1.4.4: Execute the script and verify that _site/index.html renders room statuses correctly.

## 1.5. Solutions

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

## 2.1. Theoretical Introduction

Continuous Integration (CI) operates on a fundamental contract: bad code or invalid state must never merge into the main branch or reach production.

To enforce this, pipelines implement two layers of automated gates:

```bash
[ Git Push ] ──> [ Linter / Formatter Gate (Ruff) ] ──> [ Test Suite Gate (Pytest) ] ──> Pass/Fail
```

* **Static Analysis & Linting (Ruff)**: Fast, AST-level analysis written in Rust that detects syntax bugs, unused imports, anti-patterns, and style violations across codebases.
* **Domain Invariant Testing (Pytest)**: Tests that validate business rules and data models rather than code mechanics.
  In our yoga studio, if an administrator marks a room as `status: "maintenance"` while classes are scheduled in it, the build must fail immediately with actionable feedback.

## 2.2. Steps to Complete the Chapter

* Configure Ruff in `pyproject.toml` to establish rule sets and format parameters.
* Execute Ruff checks and auto-formatting against the local codebase.
* Construct a validation module `tests/test_studio.py` containing domain assertion rules for the studio.
* Run `pytest` locally to confirm test outcomes.

## 2.3. General Exercises

* Test Ruff's linter on any python script:

```Bash
ruff check .
```

* Run Ruff format check without modifying files:

```Shell
ruff format --check .
```

* Run Pytest with concise output:

```Shell
pytest -v
```

## 2.4. Case-Specific Tasks

* **Task 2.4.1**: Create `pyproject.toml` in your project root with Ruff configuration enabling core (`E, F`), bugbear (`B`), and import sorting (`I`).
* **Task 2.4.2:** Write `tests/test_studio.py` verifying two critical business rules:
  * No class can be assigned to a room currently set to `maintenance`.
  * Registered attendees for a class cannot exceed the room's maximum capacity.
* **Task 2.4.3**: Run `ruff check .` and `ruff format .` to format all code. (use the `--fix` option if needed)
* **Task 2.4.4**: Run `pytest` to confirm all validation checks pass.

## 2.5. Solutions

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

# Chapter 3: Workflow Anatomy & Automated Quality Gates

## 3.1. Theoretical Introduction

A **GitHub Actions Workflow** is an automated, event-driven procedure defined as a YAML file inside the `.github/workflows/` directory of your repository.

```shell
┌────────────────────────────────────────────────────────┐
│ Workflow: ci.yml                                       │
│ Trigger: push / pull_request on branch 'main'          │
│                                                        │
│  Job: quality-check (runs-on: ubuntu-latest)           │
│  ├── Step 1: actions/checkout@v4                       │
│  ├── Step 2: actions/setup-python@v5                   │
│  ├── Step 3: Install dependencies (ruff, pytest)       │
│  ├── Step 4: Run Ruff linter                           │
│  └── Step 5: Run Pytest test suite                     │
└────────────────────────────────────────────────────────┘
```

### Core Components of the YAML Schema

* **`name`** : Descriptive display identifier in the GitHub Actions dashboard.
* **`on`** : Event triggers (`push`, `pull_request`, `workflow_dispatch`, etc.).
* **`jobs`** : Independent units of work running on separate virtual machines. Jobs execute in parallel by default unless explicit dependency chains (`needs:`) are declared.
* **`runs-on`** : Target OS image (e.g., `ubuntu-latest`, `windows-latest`, `macos-latest`).
* **`steps`** : Linear sequence of tasks within a job. Can execute shell commands (`run:`) or reusable marketplace actions (`uses:`).

## 3.2. Steps to Complete the Chapter

* Create the workflow directory hierarchy: `.github/workflows/.`
* Construct `ci.yml` targeting `push` and `pull_request` triggers on `main`.
* Add steps to check out code, install the Python environment, run Ruff, and execute Pytest.
* Commit and push changes to GitHub to watch the workflow execute in the Actions tab.

## 3.3. General Exercises

* Review YAML syntax rules:
  * Two spaces for indentation (no tabs).
  * Key-value pairs (`key: value`).
  * Array items denoted by `-`.
* Explore GitHub Actions step naming: Every step should have a clear, descriptive `name:` property to make debugging failed runs intuitive.

## 3.4. Case-Specific Tasks

* **Task 3.4.1:** Create `.github/workflows/ci.yml`.
* **Task 3.4.2:** Define a job `lint-and-test` targeting `ubuntu-latest`.
* **Task 3.4.3:** Use `actions/checkout@v4` and `actions/setup-python@v5` with Python version `3.11` and pip caching enabled (`cache: 'pip'`).
* **Task 3.4.4:** Add steps that run `ruff check .`, `ruff format --check .`, and `pytest`.
* **Task 3.4.5:** Commit all project files to Git, link your remote GitHub repository, push to `main`, and inspect the Actions tab.

## 3.5. Solutions

Update the folder and file structure in the local repo to include the ci.yml file

```Shell
.github/workflows/ci.yml

YAML
name: CI Quality Gate

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest

    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install ruff pytest jinja2

      - name: Run Ruff linter
        run: ruff check .

      - name: Check code formatting with Ruff
        run: ruff format --check .

      - name: Run Pytest domain safety checks
        run: pytest -v
```

**Push to GitHub:**

```Shell
git add .
git commit -m "feat: setup studio generator, ruff config, tests and CI workflow"
git remote add origin https://github.com/<YOUR-USERNAME>/prana-flow-studio.git
git push -u origin main
```

Navigate to `[https://github.com/](https://github.com/)<USER_NAME>/prana-flow-studio/actions` to monitor the pipeline execution.

# Chapter 4: Artifact Compilation in the Cloud

## 4.1. Theoretical introduction

CI pipelines do more than test; they also compile, build, and package software. In static site generation, this means executing `python build.py` directly inside the cloud runner to produce the production-ready `_site/` directory.

However, jobs in GitHub Actions run inside ephemeral virtual machines. Once a job finishes, its filesystem is destroyed. To preserve compiled build outputs, workflows use  **Artifacts** :

```Shell
[ Job: Build ] ──> Generates _site/ ──> actions/upload-pages-artifact ──> GitHub Cloud Storage
                                                                              │
[ Job: Deploy ] <────────────────── Download Artifact ────────────────────────┘
```

By decoupling the **build** step from the **deploy** step, you ensure that if tests fail or the build crashes, no deployment occurs.

## 4.2. Steps to Complete the Chapter

* Separate the workflow into distinct, sequential stages: a quality gate job followed by a build job.
* Link the build job using the `needs:` keyword so it only runs if the quality checks pass.
* Execute `python build.py` to compile the site inside the cloud runner.
* Upload the resulting `_site` directory using GitHub's specialized `actions/upload-pages-artifact@v3`.

## 4.3. General Exercises

* Understand job dependency syntax:

```YAML
job-a:
  runs-on: ubuntu-latest
  # ...
job-b:
  needs: job-a
  runs-on: ubuntu-latest
  # runs only if job-a succeeds
```

* Understand what `actions/upload-pages-artifact` does: it packages a specified directory into a compressed `github-pages` tarball artifactz specifically prepared for GitHub Pages hosting.

## 4.4. Case-Specific Tasks

* **Task 4.4.1:** Update `.github/workflows/ci.yml` (renaming it or structuring it as `deploy.yml`) to add a second job named `build`.
* **Task 4.4.2:** Establish a dependency using `needs: lint-and-test`.
* **Task 4.4.3:** Add steps to check out code, set up Python, install `jinja2`, and run `python build.py`.
* **Task 4.4.4:** Use `actions/upload-pages-artifact@v3` with `path: '_site'` to store the generated site.

## 4.5. Solutions

**Updated** `.github/workflows/deploy.yml`

*(Replace `ci.yml` with `deploy.yml`)*

```YAML
name: CI & Build Pipeline

on:
  push:
    branches: [ "main" ]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install test tools
        run: |
          python -m pip install --upgrade pip
          pip install ruff pytest jinja2

      - name: Run Ruff checks
        run: |
          ruff check .
          ruff format --check .

      - name: Run Pytest
        run: pytest -v

  build:
    needs: lint-and-test
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install generator dependencies
        run: |
          python -m pip install --upgrade pip
          pip install jinja2

      - name: Compile Studio HTML
        run: python build.py

      - name: Upload Pages Artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: "_site"
```

# 5. Continuous Deployment to GitHub Pages

## 5.1. Theoretical Introduction

Continuous Deployment (CD) is the phase where tested, built artifacts are published to production infrastructure without manual human intervention.

Historically, deploying to GitHub Pages required pushing HTML files to a dedicated `gh-pages` branch. Modern GitHub Pages uses direct, branchless deployments driven by OpenID Connect (OIDC) authentication and granular repository permissions.

```Bash
[ Push to main ] ──> [ Tests Pass ] ──> [ HTML Compiled ] ──> [ actions/deploy-pages ] ──> Live URL
```

### GitHub Pages Security & Concurrency

* **Permissions:** Deployment workflows require `pages: write` (to update your site) and `id-token: write` (to authenticate via OIDC).
* **Concurrency:** The `concurrency` block ensures that if multiple commits are pushed in quick succession, older deployments are canceled in favor of the newest build, preventing race conditions.

## 5.2. Steps to Complete the Chapter

* Configure GitHub Pages settings in your repository to use **GitHub Actions** as the build source.
* Add the final `deploy` job using `actions/deploy-pages@v4`.
* Push to `main` and verify the live website URL.
* **The Practical Simulation:** Edit `data/studio.json` locally to mark a room with active classes as `maintenance`. Push the change and watch CI stop the bad update before it deploys.

## 5.3. General Exercises

* Locate GitHub repository settings: Settings -> Pages -> Build and deployment -> Source.
* Understand the function of concurrency groups:

```YAML
concurrency:
  group: "pages"
  cancel-in-progress: false
```

## 5.4. Case-Specific Tasks

* Task 5.4.1: On GitHub, go to Settings > Pages and set Source to GitHub Actions.
* Task 5.4.2: Add the deploy job to .github/workflows/deploy.yml with the proper environment and concurrency settings.
* Task 5.4.3: Commit, push, and confirm your site is live at https://<YOUR-USERNAME></your>.github.io/prana-flow-studio/.
* Task 5.4.4 (The Real-World Test):
  * Open data/studio.json.
  * Change Lotus Room status from "active" to "maintenance". Note that classes are still scheduled there.
  * Commit and push:

    ```shell
    git commit -am "ops: mark Lotus Room as under maintenance"
    git push
    ```
  * Inspect the Actions tab: verify that the pipeline fails during the Pytest step, halting the workflow so the broken schedule never reaches your live site.
  * Fix the conflict by moving the classes to an active room or canceling them, push the fix, and watch the pipeline turn green and deploy.

## 5.5. Solutions

Complete `.github/workflow/deploy.yml`:

```YAML
name: CI/CD Pipeline - Prana Flow Studio

on:
  push:
    branches: [ "main" ]
  workflow_dispatch:

# Permissions required for GitHub Pages deployment
permissions:
  contents: read
  pages: write
  id-token: write

# Allow only one concurrent deployment, skipping runs queued between the run in-progress and latest
concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install ruff pytest jinja2

      - name: Run Ruff Linter
        run: ruff check .

      - name: Check Code Formatting
        run: ruff format --check .

      - name: Run Domain Validation Tests
        run: pytest -v

  build:
    needs: lint-and-test
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install build dependencies
        run: |
          python -m pip install --upgrade pip
          pip install jinja2

      - name: Build static site
        run: python build.py

      - name: Upload Pages artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: "_site"

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### Simulating the Broken Change & Failure

In `data/studio.json`:

```JSON
{ 
  "id": "lotus-room",
  "name": "Lotus Room",
  "capacity": 25,
  "status": "maintenance"
}
```

Push the commit:

```Shell
git commit -am "test: simulate invalid room maintenance change"
git push
```

The GitHub Actions UI will display:

```
FAILED tests/test_studio.py::test_no_classes_in_maintenance_rooms - AssertionError: 
Business rule violation: Class 'Sunrise Vinyasa' is scheduled in room 'lotus-room' which is currently under maintenance!
```
