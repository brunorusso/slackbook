# 12. vi

## 12.1 What is vi?

Scattered all around your computer are thousands of text files. To a new user, this may seem inconsequential, but almost everything in Slackware Linux uses a plain-text file for configuration. This allows users to make changes to the system quickly, easily, and intuitively. In Chapter 5, we looked at commands such as `cat` and `less` that can be used to read these files, but what if we want to modify them? For that, we need a text editor, and `vi` is more than up to the task.

In short, `vi` is one of the oldest and most powerful text editors still widely used today. It is beloved by system administrators, programmers, hobbyists, and power users worldwide.

A bit of clarification is helpful to understand what `vi` actually is on modern systems, as Slackware Linux technically does not ship with the original BSD `vi`. Instead, Slackware includes two popular `vi` "clones": `elvis` and `vim`. These clones add many modern features to `vi`, such as syntax highlighting, binary editing modes, and network support. By default, when you execute `vi` on Slackware Linux, you are launching `elvis`, so all examples in this chapter assume you are using `elvis`. If you are accustomed to another Linux distribution, you may be more familiar with `vim`. If so, you can easily change the `/usr/bin/vi` symlink to point to `/usr/bin/vim` or set up a shell alias. While `vim` is generally considered more feature-rich, `elvis` is extremely lightweight and offers more than enough functionality for most administration tasks.

`vi` is remarkably powerful, though it can feel somewhat unintuitive and challenging for new users at first. However, mastering `vi` is an essential skill for any system administrator, as `vi` (or one of its clones) is included on virtually every Linux distribution, BSD system, and UNIX variant in existence—it is even installed by default on macOS. Once you learn `vi`, you will be able to edit configuration files on almost any system without needing to install additional software.


## 12.2 The Different Modes of vi

New users are often frustrated when using `vi` for the first time. When invoked without any file arguments, `vi` displays a clean editor interface:


![image](img/vi-screen.png)

At this point, a beginner will typically begin typing and expect the pressed keys to appear directly in the document. Instead, unexpected behaviors occur—the cursor jumps around, lines disappear, or the terminal beeps.

The reason for this is simple: `vi` is a **modal editor**. Unlike traditional text editors, `vi` operates in distinct modes:

* **Command Mode (Normal Mode):** This is the default mode when `vi` starts. In Command Mode, keystrokes are interpreted as editing commands rather than literal text. Keystrokes allow you to navigate the document, delete text, copy (yank) and paste lines, search, and perform formatting.
* **Insert Mode:** In this mode, `vi` behaves like a standard text editor. Everything you type is inserted directly into the file.
* **Ex Mode (Command-line Mode):** Accessed by typing `:` while in Command Mode. This mode places the cursor on the bottom line of the screen, allowing you to save files, quit, perform global replacements, or run shell commands.

To switch from **Command Mode** to **Insert Mode**, press <kbd>i</kbd> (to insert before the cursor), <kbd>a</kbd> (to append after the cursor), or <kbd>o</kbd> (to open a new line below). To return to **Command Mode** at any time, press the <kbd>Esc</kbd> key.


## 12.3 Opening, Saving, and Quitting

Now that you understand the basic operational modes of `vi`, the first practical step is learning how to open, save, and exit files.

Opening a file is straightforward—simply pass the filename as an argument when launching `vi` from the command line:

```bash
darkstar:~$ vi chapter_12.md
```

This opens `chapter_12.md` and loads its content into a buffer. The next image show its.

![image](img/vi-buffer.png)


**Saving Changes (`:w` and `:wq`)**

To save your work, you must be in **Command Mode**. Pressing the <kbd>:</kbd> key temporarily moves the cursor to the bottom line of the screen, entering **Ex Mode** (Command-line Mode). 

* **`:w`** — Writes (saves) the buffer contents back to the file on disk.
* **`:wq`** — Writes the changes and quits `vi` in a single command.

If you want to switch to editing another file without closing `vi`, use `:e filename`:

```text
:e chapter_05.md
```

If you have unsaved changes in your current buffer, `:e` will prevent you from switching files and display a warning. You can force `vi` to discard your unsaved changes and open the new file immediately by appending an exclamation mark: **`:e!`**. Adding <kbd>!</kbd> to most Ex Mode commands forces the action, ignoring unsaved buffer warnings.


**Quitting `vi` (`:q` and `:q!`)**

To close `vi` and return to your shell prompt:

* **`:q`** — Quits `vi` (succeeds only if there are no unsaved changes).
* **`:q!`** — Forces `vi` to quit immediately, abandoning all unsaved changes.
* **`:e!`** — Reloads the original file from disk, resetting your current buffer to its last saved state.

**Quick Reference: Ex Mode Commands**

| Command | Action |
| :--- | :--- |
| `:w` | Save current changes without exiting |
| `:wq` | Save changes and exit `vi` |
| `:q` | Exit `vi` (fails if there are unsaved changes) |
| `:q!` | Force exit `vi`, discarding all unsaved changes |
| `:e filename` | Open a different file in the buffer |
| `:e!` | Revert current file to its last saved state |



## 12.4 Moving Around

Moving around in `vi` is perhaps the hardest thing for a new user to learn. `vi` does not traditionally use the directional arrow keys for cursor movement, although in Slackware Linux that is an option. Rather, movement is simply another command issued in command-mode. The reason for this is rather simple. `vi` actually predates the inclusion of directional arrow keys on keyboards. Thus, movement of the cursor had to be accomplished by using the few keys available, so the right-hand "home row" keys of <kbd>h</kbd> , <kbd>j</kbd> , <kbd>k</kbd> , and <kbd>l</kbd> were chosen. These keys will move the cursor about whenever `vi` is in command mode. Here's a short table to help you remember how they work.

| Command | Result |
| --- | --- |
| h | Move the cursor one character left. |
| j | Move the cursor one line down |
| k | Move the cursor one line up |
| l | Move the cursor one character right |

Moving around is a little more powerful than that though. Like many command keys, these movement keys accept numerical arguments. For example, <kbd>10j</kbd> will move the cursor down 10 lines. You can also move to the end or beginning of the current line with <kbd>$</kbd> and <kbd>^</kbd> , respectively.

## 12.5 Editing A Document

Now that we're able to open and save documents, as well as move around in them, it's time to learn how to edit them. The primary means of editing is to enter insert mode using either the <kbd>i</kbd> or <kbd>a</kbd> command keys. These either insert text at the cursor's current location, or append it after the cursor's current location. Once into insert mode, you can type any text normally and it will be placed into your document. You can return to command mode in order to save your changes by pressing the <kbd>ESC</kbd> key.

## 12.6 vi Cheat Sheet

Since `vi` can be difficult to learn, I've prepared a short cheat sheat that should help you with the basics until you begin to feel comfortable.

| Command | Result |
| --- | --- |
| h | Move the cursor one character left. |
| j | Move the cursor one line down |
| k | Move the cursor one line up |
| l | Move the cursor one character right |
| 10j | Move the cursor ten lines down |
| G | Move to the end of the file |
| ^ | Move to the beginning of the line |
| $ | Move to the end of the line |
| dd | Remove a line (and store it in the copy buffer) |
| 5dd | Remove 5 lines (and store them in the copy buffer) |
| dw | Remove a single word (and store it in the copy buffer) |
| 5dw | Remove five words (and store them in the copy buffer) |
| yy | Yank (copy) a line (and store it in the copy buffer) |
| yw | Yank (copy) a single word (and store it in the copy buffer) |
| 5yw | Yank five words (and store them in the copy buffer) |
| p | Paste the contents of the copy buffer at the cursor's location |
| P | Paste the contents of the copy buffer above the cursor's location |
| r | Replace a single character |
| R | Replace multiple characters |
| x | Delete a character |
| X | Delete the previous character |
| u | Undo the last action |
| :s'old'new'g | Replace all occurances of 'old' with 'new' (current line only) |
| :%s'old'new'g | Replace all occurances of 'old' with 'new' (all lines) |
| /asdf | Locate next occurance of asdf |
| :q | Quit (without saving) |
| :w | Save the current document |
| :w file | Save the current document as 'file' |
| :x | Save and quit |
