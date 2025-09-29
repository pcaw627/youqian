# Chinese Song Filter

A Python script for filtering Chinese songs from a song lyrics dataset.

## Authors

- **Phillip Williams**
- **Zilong Pan**

## Description

This script reads a CSV file containing song lyrics and filters for Chinese songs (language="zh"). It provides detailed statistics about the dataset and saves the filtered results to a new CSV file.

## Features

- Reads song lyrics from CSV format
- Filters songs by language (Chinese)
- Displays dataset statistics and language distribution
- Saves filtered results to a new CSV file
- Provides error handling and file validation

## Requirements

- Python 3.6+
- pandas library

## Installation

Install the required dependencies:

```bash
pip install -r "requirements.txt"
```

## Usage

Run the script from the command line:

```bash
python filter_chinese_songs.py
```

The script expects:
- Input file: `dataset/song_lyrics.csv`
- Output file: `chinese_songs.csv`

## File Structure

```
.
├── filter_chinese_songs.py    # Main filtering script
├── dataset/
│   └── song_lyrics.csv        # Input dataset
├── chinese_songs.csv          # Output filtered songs
└── README.md                  # This file
```

## License

MIT License

Copyright (c) 2025 Phillip Williams and Zilong Pan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.