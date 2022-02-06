"""
# what do I want this class to do?

init as a vault interface
- how does it know vault root path?
- i want to be able to get a list of all note titles that can be used for links

i want to be able to create new notes
- create new file
- option to auto-link
"""

import os
import re

class Obsidian:
    def __init__(self, vault_root_path):

        self.vault_root_path = os.path.expanduser(vault_root_path)

        if not os.path.isdir(self.vault_root_path):
            raise ValueError("Vault path does not exist")

        self.note_paths = self._get_all_note_paths()
        print(f"{len(self.note_paths)} notes found")

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
        tags: [str]; array of #tags to append to bottom of note
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
