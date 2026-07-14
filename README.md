# QuickTextInput

Efficient keyboard text input. QuickTextInput is a lightweight desktop editor
that predicts words as you type, lets you insert them with a single keystroke,
and cleans up punctuation and capitalization when you're done — then drops the
finished text on your clipboard, ready to paste anywhere.

Predictions are drawn from *your own* writing: every finished block updates a
local word-frequency database, so the suggestions get better the more you use it.

## Features

- **Smart word suggestions** — the 20 most likely completions for the word
  you're typing, ranked by how often you've used them, updated live on each
  keystroke.
- **One-keystroke selection** — press `1`–`9`, `0`, or `F1`–`F10` to insert the
  matching suggestion.
- **One-touch cleanup** — press `F12` to finalize the text: punctuation spacing
  is normalized, sentences are capitalized, trailing periods are added, and open
  quotes are closed. URLs are left untouched.
- **Seamless clipboard integration** — finalized text is copied to the clipboard
  automatically so you can paste it straight into another application.
- **Learns from you** — finalized words are counted into a local SQLite database
  that drives future predictions.

## How it works

1. Type into the main text area. As you type a word, the panel on the left shows
   ranked completions.
2. Press the number or function key next to a suggestion to accept it (it
   replaces the partial word and adds a trailing space).
3. When the text is ready, press **F12** (or the ✓ toolbar button / *Done*). The
   text is grammar-corrected, copied to the clipboard, cleared from the editor,
   and its words are folded into your frequency database.

Suggestions only appear while the cursor is at the end of the text and you're
typing letters — they never linger.

## Platforms

QuickTextInput runs anywhere Python and Tkinter do:

- 🖥️ **Windows**
- 🍏 **macOS**
- 🐧 **Linux**

The default database path (`~/Documents/QuickTextInput.db`) resolves correctly on
all three.

## Requirements

- Python 3
- [Pillow](https://pypi.org/project/Pillow/) (for the toolbar icons)
- Tkinter (bundled with most Python installations)

```sh
pip install pillow
```

## Usage

```sh
python QuickTextInput.py
```

By default the word database lives at `~/Documents/QuickTextInput.db`
(`%USERPROFILE%\Documents\QuickTextInput.db` on Windows). Point it elsewhere
with:

```sh
python QuickTextInput.py --db path/to/words.db
```

### Seeding predictions from existing text

The database starts empty, so predictions only appear once it has learned some
words. To bootstrap it, import a corpus of your own writing:

```sh
python import-corpus.py mytext.txt
python import-corpus.py mytext.txt --db path/to/words.db
```

`import-corpus.py` counts the words in the given text file and merges them into
the database. (It uses `words.txt` as a reference list of known lowercase words
to normalize casing.)

## Building a standalone executable

On Windows, `build.bat` produces a single-file executable with PyInstaller:

```sh
build.bat
```

which runs:

```sh
pyinstaller --onefile -w QuickTextInput.py
```

## Project layout

| Path | Purpose |
| --- | --- |
| `QuickTextInput.py` | The Tkinter application. |
| `common.py` | SQLite database initialization. |
| `import-corpus.py` | Seeds the word database from a text file. |
| `words.txt` | Reference word list used to normalize casing on import. |
| `baseline_*_black_24.png` | Toolbar icons. |
| `build.bat` | PyInstaller build script (Windows). |
| `index.html`, `styles.css`, `script.js` | Marketing/landing page for the project. |
| `screenshots/` | Screenshots used by the landing page and docs. |

## License

See [LICENSE](LICENSE).

---

© Lumagraph Limited
