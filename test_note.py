from obsidian.core import Note, Obsidian

obsidian = Obsidian("~/obsidian-main")

note1 = Note(obsidian, "", "vim")

note2 = Note(obsidian, "", "xxx_test_note_xxx")
note2.update(body="this is my body", tags=[])
note2.update(body="new body", tags=["#tool", "#robot"])
note2.update(body="all three", tags=["#tool", "#robot"], header={"aliases": ["final_test"]})
note2.delete()
