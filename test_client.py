from obsidian.core import Obsidian

obsidian = Obsidian('~/obsidian-main')

new_note = obsidian.new_note(
    note_path="",
    title="zzz_test_zzz",
    body="here is my handle",
    tags=["#here", "#is", "#my", "#spout"],
    header={"aliases": ["first_alias", "second_alias"]},
    overwrite=True,
    autolink_notes=True
)

new_note.delete()
