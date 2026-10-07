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
