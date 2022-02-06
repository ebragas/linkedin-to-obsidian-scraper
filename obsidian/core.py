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

class Obsidian:
    def __init__(self, vault_root_path):
        
        self.vault_root_path = os.path.expanduser(vault_root_path)
        
        if not os.path.isdir(self.vault_root_path):
            raise ValueError("Vault path does not exist") 

        self.note_paths = self._get_all_note_names()

        print(f"{len(self.note_paths)} notes found")

    def _get_all_note_names(self):
        """return a data struct containing note names that can be linked to when creating new notes"""
        # TODO: this should probably return a data struct that can include alises
        note_names = []

        for r, d, f in os.walk(self.vault_root_path):
            for file in f:
                if file.endswith(".md"):
                    note_names.append(os.path.join(r, file))

        return note_names

    def new_note(self, note_path, title, body, tags=[], overwrite=False):
        """
        where do I want note formatting to take place?
        I think that's something specific to the data output by the LinkedIn bot, not to Obsidian
        KISS
        """
        full_note_path = os.path.join(note_path, title)

        # raise error if note already exists and overwrite=False
        if os.path.exists(full_note_path) and not overwrite:
            raise ValueError("This note already exists")

        # create note
        with open(full_note_path, 'w') as f:
            f.write(body)
            f.write('\n')
            f.write(' '.join(tags))

        self.note_paths.append(full_note_path)

        print(f"created new note: {full_note_path}")
