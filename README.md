# ACAKADUTZ (Alpha)

Random Video Shuffle Combiner

ACAKADUTZ is a small experimental desktop tool that randomly combines multiple short videos into a single long video.

This project started as a simple personal tool to solve a workflow problem: combining many short narration videos into longer videos without manually arranging them in video editing software.

This **Alpha version** is the earliest prototype and was mainly built for personal use.

---

# What This Tool Does

ACAKADUTZ takes a collection of short video clips and randomly merges them into a single longer video.

Every render produces a different result because the order of the clips is shuffled randomly.

Example workflow:

You have:

30 short narration videos  
Each video: 10–15 minutes

Using ACAKADUTZ you can randomly combine:

4–5 clips

to create a video around:

~1 hour long

Since the order is random, each output video will be different.

---

# Why This Tool Exists

Manually combining many clips in video editing software can be repetitive and time consuming.

This tool automates that process by randomly selecting and merging clips.

It was originally built to speed up the production of long-form narration content.

---

# Alpha Version Notes

This version is an **early prototype**.

Limitations may include:

• minimal user interface  
• limited error handling  
• basic rendering workflow  
• experimental performance  

Future versions may include improvements and new features.

---

# Requirements

This tool requires:

Python 3.8 or newer

FFmpeg installed and available in PATH.

Download FFmpeg:

https://ffmpeg.org/download.html

Verify installation:

```
ffmpeg -version
```

---

# Installation

Clone the repository:

```
git clone https://github.com/yourusername/ACAKADUTZ.git
```

Enter the project directory:

```
cd ACAKADUTZ
```

Install dependencies:

```
pip install -r requirements.txt
```

Run the application:

```
python app.py
```

---

# Basic Usage

1. Select the folder containing video clips
2. Choose how many clips should be combined
3. Start the render process
4. The tool will randomly shuffle and merge clips

Each render produces a different video.

---

# Version

```
ACAKADUTZ Alpha
Initial experimental build
```

# Screenshot

![ACAKADUTZ UI](assets/screenshot-ui.png)

---

# Disclaimer

This software is provided as an experimental tool.

It may contain bugs or unfinished features.

Use at your own risk.

---

# Author

Created as a personal utility tool to simplify long-form video creation from short narration clips.

If you find this tool useful, feel free to share it with others.
