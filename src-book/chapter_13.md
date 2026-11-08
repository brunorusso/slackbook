# 13. Emacs

## 13.1 What is Emacs?

`vi` and its clones are functional, fast, and powerful text editors. However, traditional `vi` is not particularly extensible. While `vim` breaks this trend by being both lightweight and highly extensible, many users prefer an editor with even greater customization capabilities and built-in features. This is why many system administrators and programmers prefer **GNU Emacs**.

`Emacs` takes extensibility to the next level. Outside of a minimal core written in C for performance, the vast majority of `Emacs` is written in **Emacs Lisp** (Elisp)—a dialect of the Lisp programming language. Nearly all of `Emacs` is exposed to the user, allowing you to configure, tweak, or completely extend the editor at will.

Over the decades, the community has written an incredible variety of extensions in Emacs Lisp, ranging from syntax highlighting for obscure languages to full web browsers, email clients, and terminal emulators. In fact, `Emacs` even includes a `vi` emulation mode (such as `viper` or `evil-mode`), allowing you to enjoy modal editing while leveraging the underlying power of the `Emacs` environment.

Like `vi`, there are multiple implementations of `Emacs` (collectively referred to as "emacsen"). However, the most widely used variant—and the one included with Slackware Linux—is **GNU Emacs**. When people mention "Emacs", they are almost always referring to GNU Emacs.

Unlike `vi`, `Emacs` operates more like a traditional editor by default. It is modeless, meaning most actions and keyboard shortcuts are performed using modifier keys (such as <kbd>Ctrl</kbd> and <kbd>Alt</kbd>) without needing to switch between Command and Insert modes. You can open a file and immediately begin typing without worrying about which operational mode is active.


## 13.2 Starting Out

`Emacs` can be started simply by running the `emacs` command in your terminal. When launched in a console without any arguments, `Emacs` displays a startup screen containing helpful documentation links and tutorial options.


![image](img/emacs.png)

If you are running the X Window System, `Emacs` may launch its graphical user interface (GUI) by default. If you prefer running it directly inside your terminal console, invoke it with the `-nw` (*no window*) flag:

```bash
darkstar:~$ emacs -nw
```

While on the startup screen, you can navigate using the keyboard arrow keys. Underlined items are links that can be activated by moving the cursor over them and pressing <kbd>Enter</kbd>.

**Understanding Emacs Key Notation**

`Emacs` keyboard shortcuts rely heavily on modifier keys and use a specific shorthand notation throughout manuals and built-in help:

- `C- (Control)`: Hold down the <kbd>Ctrl</kbd> key while pressing the specified key. For example, <kbd>C-h</kbd> means holding <kbd>Ctrl</kbd> and pressing <kbd>h</kbd>.
- `M- (Meta)`: Hold down the <kbd>Meta</kbd> key (mapped to <kbd>Alt</kbd> on modern keyboards) or press <kbd>Esc</kbd> before the key. For example, <kbd>M-x</kbd> means holding <kbd>Alt</kbd> and pressing <kbd>x</kbd>.
- `Sequential Key Combinations`: Sequences such as <kbd>C-x C-c</kbd> mean holding <kbd>Ctrl</kbd> and pressing <kbd>x</kbd>, then holding <kbd>Ctrl</kbd> and pressing <kbd>c</kbd>. Conveniently, <kbd>C-x C-c</kbd> is the command to save modified buffers and exit Emacs.


**Opening, Editing, and Saving Files**

You can also launch `Emacs` directly with a filename as an argument:

```bash
darkstar:~\$ emacs chapter_13.md
```

**Saving Files (C-x C-s)**

To save your changes back to disk, press <kbd>C-x C-s</kbd>.

If you are creating a new file, `Emacs` will prompt you for a filename in the minibuffer—the single text input line located at the very bottom of the screen. Type your desired filename and press <kbd>Enter</kbd>.

If you make a mistake or want to cancel any active minibuffer prompt, press <kbd>C-g</kbd> to abort the current command.

> Note: Tab completion is available in the minibuffer for filenames and command names.


**Managing Files and Buffers (C-x C-f, C-x b, C-x C-b)**

In `Emacs`, open files are held in memory structures called buffers.

- Opening or Creating Files (C-x C-f): Press <kbd>C-x C-f</kbd> (find-file) to open another file within the same Emacs session. Enter the file path in the minibuffer. If the file does not exist, Emacs creates a new buffer for it, which will be written to disk when saved (<kbd>C-x C-s</kbd>).
- Switching Buffers (C-x b): Opening a new file does not close previously opened files. To switch back to an open buffer, press <kbd>C-x b</kbd> (switch-to-buffer), type the buffer name in the minibuffer, and press <kbd>Enter</kbd>.
- Listing All Buffers (C-x C-b): Press <kbd>C-x C-b</kbd> (list-buffers) to open a split window displaying all active buffers.

## 13.3 How to Move Around

Like `vi`, `Emacs` predates dedicated arrow keys on standard computer keyboards. While modern implementations of `Emacs` fully support navigation via arrow keys, using native keyboard shortcuts allows you to move through files efficiently without taking your hands off the main typing row.

While `vi` movement keys (`h`, `j`, `k`, `l`) focus on ergonomic home-row positioning, `Emacs` movement keys are **mnemonic**—designed around the first letter of each corresponding motion:

* **`f`** = **F**orward
* **`b`** = **B**ackward
* **`n`** = **N**ext line
* **`p`** = **P**revious line

Below is a reference of basic character and line movement keybindings:


| Command | Action |
| --- | --- |
| <kbd>C-f</kbd> | Move the cursor one character to the right (**f**orward) |
| <kbd>C-b</kbd> | Move the cursor one character to the left (**b**ackward) |
| <kbd>C-n</kbd> | Move the cursor one line down (**n**ext) |
| <kbd>C-p</kbd> | Move the cursor one line up (**p**revious) |


**Repeating Movement Commands**

Just as with `vi`, you can repeat movement actions by passing a numeric multiplier:

* **Using the Universal Argument (`C-u`):** Type <kbd>C-u</kbd> followed by a number and the movement command. For example, <kbd>C-u 10 C-p</kbd> moves the cursor up 10 lines, and <kbd>C-u 5 C-f</kbd> moves it 5 characters forward.
* **Using Meta Digits (`M-`):** Hold the <kbd>Meta</kbd> (<kbd>Alt</kbd>) key while typing the numbers. For example, <kbd>M-1 M-0 C-p</kbd> moves the cursor 10 lines up, and <kbd>M-5 C-f</kbd> moves it 5 characters to the right.



## 13.4 Getting Help


`Emacs` contains an extensive built-in help system, to the point that it is often described as a "self-documenting" editor. This is because it provides interactive mechanisms to inspect keybindings, look up function descriptions, and search manual topics directly within your editing session without needing an external browser or terminal.

All help commands share the **<kbd>C-h</kbd>** prefix. Below are some of the most useful documentation functions:


| Command | Action |
| --- | --- |
| <kbd>C-h t</kbd> | Open the interactive **Emacs Tutorial** |
| <kbd>C-h f</kbd> `FUNCTION-NAME` <kbd>Enter</kbd> | Display documentation for a specific function |
| <kbd>C-h k</kbd> `KEY-SEQUENCE` | Describe the function bound to a key sequence (e.g., <kbd>C-h k C-x C-c</kbd>) |
| <kbd>C-h ?</kbd> | Display a list of all available help options |


The interactive tutorial launched by **<kbd>C-h t</kbd>** is especially recommended if you are new to `Emacs` and need hands-on practice with basic navigation and text manipulation commands.


## 13.5 Calling Functions

As noted earlier, `Emacs` exposes a vast number of internal functions for interactive use. Many common actions—such as opening or saving files—are bound directly to keyboard shortcuts. However, thousands of other functions (such as toggling display modes or navigating to specific positions) are not bound to any default key combination.

To execute any interactive function by name, press **<kbd>M-x</kbd>** (*execute-extended-command*). This opens a prompt in the minibuffer at the bottom of the screen where you can type the function name and press <kbd>Enter</kbd>.

For example, to move the cursor to the end of the current line using its function name, you would press:

<kbd>M-x</kbd> `end-of-line` <kbd>Enter</kbd>

The cursor immediately moves to the end of the line.

> Note: Tab completion is fully supported in the minibuffer when typing function names after pressing <kbd>M-x</kbd>, making it easy to search for and run commands even if you only remember part of their name.


## 13.6 Emacs Cheat Sheet

While `Emacs` can be simple to use once you get the hang of basic concepts, its vast scope can easily feel overwhelming. Below is a categorized reference guide covering the most essential `Emacs` commands. 

> Note: Advanced features, detailed selection modes, and customization options are fully documented in the built-in `Emacs` manual (<kbd>C-h r</kbd>) and online tutorials.

**Cursor Movement & Navigation**

| Command | Action |
| --- | --- |
| <kbd>C-f</kbd> / <kbd>C-b</kbd> | Move cursor forward / backward one character |
| <kbd>C-n</kbd> / <kbd>C-p</kbd> | Move cursor down / up one line |
| <kbd>M-f</kbd> / <kbd>M-b</kbd> | Move cursor forward / backward one word |
| <kbd>C-a</kbd> / <kbd>C-e</kbd> | Jump to the beginning / end of the current line |
| <kbd>M-x beginning-of-line</kbd> | Move to beginning of current line (via function call) |
| <kbd>M-x end-of-line</kbd> | Move to end of current line (via function call) |
| <kbd>M-<</kbd> / <kbd>M-></kbd> | Jump to the beginning / end of the buffer |
| <kbd>M-1 M-0 C-n</kbd> (or <kbd>C-u 10 C-n</kbd>) | Move down 10 lines (using numeric argument) |


**Editing, Selection & Kill Ring (Copy / Cut / Paste)**

| Command | Action |
| --- | --- |
| <kbd>C-Space</kbd> | Set mark to start text selection (press again to toggle selection mode) |
| <kbd>C-w</kbd> | **Cut** (kill) selected region and store it in the kill ring |
| <kbd>M-w</kbd> | **Copy** selected region into the kill ring |
| <kbd>C-y</kbd> | **Paste** (yank) the contents of the kill ring at cursor position |
| <kbd>C-k</kbd> | Kill text from cursor position to the end of the current line |
| <kbd>C-/</kbd> | **Undo** previous action (includes stepping back through undo history) |
| <kbd>Insert</kbd> | Toggle between Insert mode and Overwrite mode |
| <kbd>C-g</kbd> | **Cancel** current operation or active minibuffer prompt |


**Incremental Search & Replace**

| Command | Action |
| --- | --- |
| <kbd>C-s</kbd> `text` <kbd>Enter</kbd> | Search **forward** incrementally for `text` (press <kbd>C-s</kbd> again for next match) |
| <kbd>C-r</kbd> `text` <kbd>Enter</kbd> | Search **backward** incrementally for `text` (press <kbd>C-r</kbd> again for previous match) |
| <kbd>M-%</kbd> `old` <kbd>Enter</kbd> `new` <kbd>Enter</kbd> | Query replace `old` with `new` (press <kbd>y</kbd> to replace, <kbd>n</kbd> to skip, <kbd>!</kbd> for all) |


**Help, Commands & Menu Bar**

| Command | Action |
| --- | --- |
| <kbd>C-h t</kbd> | Launch the interactive **Emacs Tutorial** |
| <kbd>C-h f</kbd> `FUNCTION-NAME` <kbd>Enter</kbd> | Display documentation for a specific function |
| <kbd>C-h k</kbd> `KEY-SEQUENCE` | Show documentation for the function bound to a key sequence |
| <kbd>C-h ?</kbd> | Display all available help functions |
| <kbd>M-x</kbd> `FUNCTION-NAME` <kbd>Enter</kbd> | Call an interactive function by name |
| <kbd>M-`</kbd> | Access the top menu bar from terminal mode |


**File & Session Management**

| Command | Action |
| --- | --- |
| <kbd>C-x C-f</kbd> | Open (find) a file or create a new buffer |
| <kbd>C-x C-s</kbd> | Save current buffer to disk |
| <kbd>C-x C-w</kbd> `new-file.txt` <kbd>Enter</kbd> | "Save As" (write buffer contents to `new-file.txt`) |
| <kbd>C-x C-c</kbd> | **Exit Emacs** (prompts to save modified buffers before quitting) |
