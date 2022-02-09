from jinja2 import Template

with open('templates/basic_note.md', 'r') as f:
    template = Template(f.read())

parameters = {
    "header": "YAML!",
    "tags": " ".join(["#one", "#two", "#three"]),
    "body": "Full on body"
}

print(template.render(parameters))
