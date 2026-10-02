# 13. Emacs

## 13.1 What is Emacs?

`vi` and its clones are very functional and powerful editors. However, they are often considered not particularly extensible. `vim` is a successful and powerful `vi` variant that shrugs this trend, being both extremely extensible and lightweight. However, many users prefer a more "heavy" and extensible editor. This is why many people (including the author of this chapter) prefer `Emacs` .

Emacs takes extensibility up to eleven. Outside of a core of C, the rest of `Emacs` is written in a Lisp variant, nearly all of which is exposed to you, so that you may configure it or even extend it at will (many good Emacs Lisp tutorials can be found on the Internet). People have written all sorts of extensions in Emacs Lisp, from syntax highlighting for an obscure language, to a built-in terminal. In fact, there's even a `vi` emulation mode within `Emacs` (called viper), so you can still get the modal editing that comes with vi, while having access to the power of the `Emacs` core.

Like `vi` , there are many variants of `Emacs` (termed "emacsen"). However, the one most commonly used (and the only one in Slackware) is GNU Emacs. When people reference "Emacs" directly, they almost always mean GNU Emacs.

Unlike `vi` , `Emacs` operates more like a traditional editor by default. This means that most keyboard shortcuts can be performed without repeatedly changing modes. You can open up a file and start typing away without having to learn what the modes do, or forgetting which one you are currently using.

## 13.2 Starting Out

`Emacs` can be started simply by running the `emacs` command in your terminal. When you first start it in a console without arguments, you will see something that resembles this:

If you are in X windows, `Emacs` may start a GUI instead of running in your console. If this is the case and you don't want a GUI, you can invoke it with the flag `'-nw'` .

While here, you can browse around using the keyboard arrow keys. Underlined elements are links, and you can activate them by moving over them and pressing 'enter'. The documentation mentioned is very good, and can help you get your bearings should you have any problems. Also note how they describe key sequences such as <kbd>C-h</kbd> , meaning press the <kbd>h</kbd> key while holding down the <kbd>CTRL</kbd> key. Same deal with <kbd>M-`</kbd> , meaning to hold the the <kbd>Meta</kbd> key (usually " <kbd>Alt</kbd> ") and press the backtick "`" key. When they say (e.g.) <kbd>C-x C-c</kbd> , this means to press the "x" key while holding down the <kbd>CTRL</kbd> key, then press the "x" key while also holding down the <kbd>CTRL</kbd> key. Conveniently, this is also one of the more important commands in `Emacs` : to close it.

Alternatively, if you call `emacs` with a file name as an argument, it will open that file, just like `vi` . Upon doing this, you will be presented with the contents of the file in question. Here, you can navigate the document using traditional arrow keys and type in information at will without any issues.

Say you make some edits, and you now want to save your file. The following key sequence will do that: <kbd>C-x C-s</kbd> . If you made a new file, you will be prompted for this in what is called the "minibuffer", the blank line below the gray line at the bottom of the screen. Type in the file name of your choice, then hit <kbd>Enter</kbd> . If you don't want to save the file, you can press <kbd>C-g</kbd> , which aborts operations that ask for input. Do note that tab-completion is usually available for operations that use the minibuffer.

Should you want to open a new file within your same `Emacs` session, type in <kbd>C-x C-f</kbd> . You will be prompted for a file name in the minibuffer. `Emacs` doesn't care whether it exists or not. If it doesn't exist, a new buffer will be created for it (the file will be created upon saving with <kbd>C-x C-s</kbd> ), or it will be opened as expected. However, the old file will still be open! You can switch back to it using <kbd>C-x C-b</kbd> , entering in the file's name (or more technically, the buffer's name), then hitting <kbd>Enter</kbd> .

## 13.3 How to Move Around

Like `vi` , `Emacs` is also older than the arrow keys on your keyboard. Also, like in `vi` , using the arrow keys to navigate files is also supported. While the `vi` movement keys are more ergonomic, `emacs` 's are more "mnemonic". However, it is still very possible to operate using the main `Emacs` keybindings quickly and efficiently. Here is a table of the basic movement keybindings:

| Command | Result |
| --- | --- |
| C-f | Move the cursor one character to the right (forward) |
| C-b | Move the cursor one character to the left (backward) |
| C-n | Move the cursor one line down (next) |
| C-p | Move the cursor one line up (previous) |

Of course, like with `vi` it is also possible to repeat these commands with a numeric argument. If you type in <kbd>M-1 M-0 C-p</kbd> , or <kbd>C-u 10 C-p</kbd> , the cursor will move ten lines up. If you type in <kbd>M-5 C-f</kbd> or <kbd>C-u 5 C-f</kbd> , the cursor will move five characters to the right.

## 13.4 Getting Help

`Emacs` contains a great deal of documentation, to the point that it is often called a "self-documenting" editor. This is because it provides mechanisms for providing users with documentation while you are using it. Here are some useful functions that display documentation (they all start with <kbd>C-h</kbd> ):

| Command | Result |
| --- | --- |
| C-h f FUNCTION-NAME Enter | Show documentation for function FUNCTION-NAME |
| C-h k C-x C-c | Show documentation for the function bound to the keys C-x C-c |
| C-h t | Show the Emacs tutorial |
| C-h ? | Show all help-related functions |

<kbd>C-h t</kbd> is especially useful if you want or need practice using `Emacs` .

## 13.5 Calling Functions

As noted earlier, `Emacs` exports a large number of functions to for interactive use. Some of these, like those opening and saving files, are mapped to keys. Others (like the ones for moving to the beginning and end of lines) are not. To call them, you have to invoke them. Say we want to call the function "end-of-line". We would do this:

<kbd>M-x end-of-line Enter</kbd>

And the cursor would move to the end of the line, as the function name suggests.

## 13.6 Emacs Cheat Sheet

While Emacs can be simple to use, its scope can easily be overwhelming. Below are some useful Emacs commands. Some aspects have been simplified, most notably regarding text selection. These concepts, and more, are described the `Emacs` manual, and various on-line tutorials. Decent summaries can also be gleaned from web searches.

| Command | Result |
| --- | --- |
| C-f | Move the cursor one character to the right (forward) |
| C-b | Move the cursor one character to the left (backward) |
| C-n | Move the cursor one line down (next) |
| C-p | Move the cursor one line up (previous) |
| C-h f FUNCTION-NAME Enter | Show documentation for function FUNCTION-NAME |
| C-h k C-x C-c | Show documentation for the function bound to the keys C-x C-c |
| C-h t | Show the Emacs tutorial |
| C-h ? | Show all help-related functions |
| M-` | Access the Menu Bar |
| C-g | Cancel the current operation. This is most useful when in the minibuffer. |
| M-x FUNCTION-NAME Enter | Call the interactive function FUNCTION-NAME |
| M-1 M-0 C-n | Move the cursor ten lines down |
| C-u 10 C-n | Move the cursor ten lines down (same as above) |
| M-x beginning-of-line | Move the cursor to the beginning of the current line |
| M-x end-of-line | Move the cursor to the end of the current line |
| M-> | Move the cursor to the end of the buffer |
| M-< | Move the cursor to the beginning of the buffer |
| C-k | Remove text from the cursor to the end of the line and place it into the kill ring |
| C-space | Enter selection mode (use normal motion keys to move around). Press C-space again to leave it. |
| C-w | While in selection mode, delete the selected region, and store the result into the kill ring |
| M-w | While in selection mode, store the selected region into the kill ring. |
| C-y | "Yanks" the contents of the kill ring and places them at the cursor's location |
| C-/ | Undo the previous action. Unlike most other editors, this includes previous undo actions. |
| insert | Enable or disable overwriting characters |
| C-s asdf Enter | Forward incremental search for the string "asdf". Repeat C-s as needed to search for future items, or C-r (below) to search backwards. |
| C-r asdf Enter | Backward incremental search for the string "asdf". Repeat C-r as needed to search for future items, or C-s (above) to search forwards. |
| M-% old Enter new Enter | Search for each instance of "old" and prompt you to replace it with "new". You can force replacement of all items by typing "!" at the replacement prompt. |
| C-x C-c | Exit Emacs, prompting you to save each unsaved buffer before doing so |
| C-x C-s | Save the currrent buffer to its file |
| C-x C-w new-file.txt Enter | Save the current buffer to a file "new-file.txt" |
