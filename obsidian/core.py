"""
# what do I want this class to do?

init as a vault interface
- how does it know vault root path?
- i want to be able to get a list of all note titles that can be used for links

i want to be able to create new notes
- create new file
- option to auto-link
"""

from importlib.resources import path
import os
import re
import yaml
from jinja2 import Template, Environment

environment = Environment(trim_blocks=True)


class Obsidian:
    def __init__(self, vault_root_path):
        """Initialize Obsidian client for a single vault."""
        self.vault_root_path = os.path.expanduser(vault_root_path)

        if not os.path.isdir(self.vault_root_path):
            raise ValueError("Vault path does not exist")

        self.note_paths = self._get_all_note_paths()
        self.notes = [Note(self, *os.path.split(path)) for path in self.note_paths]
        
        print(f"{len(self.notes)} notes found")

    def _get_all_note_paths(self):
        """return a data struct containing note names that can be linked to when creating new notes"""
        # TODO: this should probably return a data struct that can include alises
        note_names = []

        for r, d, f in os.walk(self.vault_root_path):
            for file in f:
                if file.endswith(".md"):
                    note_names.append(os.path.join(r, file))

        return note_names

    def _link_text(self, text):
        """string word replacement for linking"""
        # use regext because i need to replace whole words only
        link_strings = [os.path.splitext(os.path.basename(path))[0] for path in self.note_paths]

        linked_text = text

        for link in link_strings:
            linked_text = re.sub(r"\b%s\b" % link, f"[[%s]]" % link, linked_text)

        # replace and quadruple brackets w/ double brackets
        linked_text = linked_text.replace("[[[[", "[[")
        linked_text = linked_text.replace("]]]]", "]]")

        return linked_text

    def new_note(self, note_path, title, body, tags=[], overwrite=False, autolink_notes=True):
        """
        note_path: str; relative to vault root path
        title: str; name of note/file
        body: str; markdown contents of note
        tags: [str]; array of #tags to append to note
        overwrite: bool; whether to allow existing notes to be overwritten (default False)
        autolink_notes: bool; whether to find keywords in note body that match existing notes, and turn them into internal links

        where do I want note formatting to take place?
        I think that's something specific to the data output by the LinkedIn bot, not to Obsidian
        KISS
        """
        full_note_path = os.path.join(self.vault_root_path, note_path, title + '.md')

        # raise error if note already exists and overwrite=False
        if os.path.exists(full_note_path) and not overwrite:
            raise ValueError("This note already exists")

        if autolink_notes:
            body = self._link_text(body)

        # create note
        with open(full_note_path, 'w') as f:
            f.write(body)
            f.write('\n')
            f.write(' '.join(tags))

        self.note_paths.append(full_note_path)

        print(f"created new note: {full_note_path}")



class Note:

    templates_dir = 'templates/'

    def __init__(self, obsidian, path, name):
        """Either load note components from existing file, or create new one.

        obsidian: Obsidian
        path: String relative path to note
        name: String title of note/file name

        TODO: use template for writing notes
        """
        self.obsidian = obsidian
        self.path = path
        self.name = name
        if not name.endswith(".md"):
            self.name = self.name + ".md"
        self.full_path = self._note_full_path()

        # note components
        self.header = {}
        self.tags = []
        self.body = ""

        if os.path.exists(self.full_path):
            self.header, self.tags, self.body = self._parse_note_from_md()
        else:
            with open(self.full_path, "w") as f:
                pass

    def __repr__(self):
        return f"<Note: {self.path}"

    def _note_full_path(self):
        """Return full file path of note"""
        return os.path.join(os.path.expanduser(self.obsidian.vault_root_path),
                            self.path,
                            self.name
                            )

    def _parse_note_from_md(self):
        """Parse the contents of note from file"""
        header = {}
        tags = []
        body = ""
        yaml_end_idx = 0

        with open(self.full_path, "r") as f:
            text_lines = f.readlines()

        if text_lines:

            # parse out YAML header
            if text_lines[0] == "---\n": # then there's YAML

                # find next ---
                for i, line in enumerate(text_lines[1:]):
                    if line == "---\n":
                        yaml_end_idx = i + 1
                        break

                # all lines between are YAML
                yaml_string = '\n'.join(text_lines[1:yaml_end_idx])
                header = yaml.safe_load(yaml_string)

            body_lines = text_lines[yaml_end_idx + 1:]

            # drop empty lines in beginning of body
            for i, line in enumerate(body_lines):
                if line.strip():
                    body_lines = body_lines[i:]
                    break

            body = "".join(body_lines)

            # find tags
            tags = re.findall("(#+[a-zA-Z0-9(_)]{1,})", body)

        return header, tags, body

    def _write_note(self, template='basic_note.md'):
        """Write components to file
        """
        with open(os.path.join(self.templates_dir, template), 'r') as f:
            template = Template(f.read(), trim_blocks=True)

        parameters = {
            "header": self.header,
            "tags": " ".join(self.tags),
            "body": self.body
        }

        note_text = template.render(parameters)

        with open(self.full_path, 'w') as f:
            f.write(note_text)

    def update(self, body=None, tags=None, header=None):
        """Update the note components
        """
        self.header = header if header else self.header
        self.body = body if body else self.body
        self.tags = tags if tags else self.tags
        self._write_note()

    def append(self, body, tags):
        """Append the arguments to their corresponding note component
        """
        self.body = self.body + "\n" + body
        self.tags.append(tags)
        self._write_note()

    def delete(self):
        """Kill with fire."""
        os.remove(self.full_path)
