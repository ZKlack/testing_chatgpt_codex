# Study Manager

A simple CLI tool to manage study notes. Notes can include text or file attachments and support tagging by course and chapter. Each note has a `max_cooldown` which determines the number of days until it is due again, skipping configured off days.

## Features
- Create new notes
- Fetch due notes
- Increase or reset the cooldown of a note

Run `python -m studymanager.cli --help` for usage instructions.

