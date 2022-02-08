"""
Add tags to directories based on a map if they don't already exist
# remember to skip YAML section at top of notes
# maybe I want to not do this right now and instead work on the obisidan class so I can build capability for this
"""
import os

VALUE_ROOT_DIR = "~/obsidian-main"

tag_map = {
    "data/data engineering/tools": ["#tool"],
    "data/machine learning/tools": ["#tool"],

}
