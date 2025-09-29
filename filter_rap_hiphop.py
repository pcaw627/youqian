#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chinese Rap & Hip-Hop Song Filter Script

This script reads chinese_songs.csv, filters for rap and hip-hop songs,
and saves the results to chinese_raphiphop.csv.
"""

import pandas as pd
import os
import sys
import re

def filter_rap_hiphop_songs(input_file, output_file):
    """
    Filter CSV file for rap and hip-hop songs and save to new file
    
    Args:
        input_file (str): Path to input CSV file
        output_file (str): Path to output CSV file
    """
    try:
        # Read the CSV file
        print(f"Reading CSV file: {input_file}")
        df = pd.read_csv(input_file)
        
        # Display basic info about the dataset
        print(f"Total Chinese songs: {len(df)}")
        print(f"Columns: {list(df.columns)}")
        
        # Check if 'tag' column exists
        if 'tag' not in df.columns:
            print("Error: 'tag' column not found in the CSV file")
            print("Available columns:", list(df.columns))
            return False
        
        # Display tag distribution
        print("\nTag distribution:")
        tag_counts = df['tag'].value_counts()
        print(tag_counts.head(20))  # Show top 20 tags
        
        # Filter for rap and hip-hop songs
        # Create a case-insensitive pattern for rap and hip-hop related tags
        rap_hiphop_pattern = r'(rap|hip.?hop|hiphop|嘻哈|说唱|饶舌)'
        
        # Filter using the pattern
        rap_hiphop_songs = df[df['tag'].str.contains(rap_hiphop_pattern, case=False, na=False)]
        
        print(f"\nRap/Hip-Hop songs found: {len(rap_hiphop_songs)}")
        
        if len(rap_hiphop_songs) == 0:
            print("No rap/hip-hop songs found in the dataset")
            print("Available tags:", df['tag'].unique()[:20])  # Show first 20 unique tags
            return False
        
        # Display the unique tags found
        print("\nRap/Hip-Hop tags found:")
        unique_tags = rap_hiphop_songs['tag'].value_counts()
        print(unique_tags)
        
        # Save filtered data to new CSV
        rap_hiphop_songs.to_csv(output_file, index=False, encoding='utf-8')
        print(f"\nRap/Hip-Hop songs saved to: {output_file}")
        
        # Display sample of filtered data
        print("\nSample of Rap/Hip-Hop songs:")
        sample_data = rap_hiphop_songs[['title', 'artist', 'year', 'tag']].head(10)
        print(sample_data.to_string(index=False))
        
        # Display year distribution
        if 'year' in rap_hiphop_songs.columns:
            print(f"\nYear distribution of Rap/Hip-Hop songs:")
            year_dist = rap_hiphop_songs['year'].value_counts().sort_index()
            print(year_dist)
        
        # Display artist distribution
        if 'artist' in rap_hiphop_songs.columns:
            print(f"\nTop 10 Rap/Hip-Hop artists:")
            artist_dist = rap_hiphop_songs['artist'].value_counts().head(10)
            print(artist_dist)
        
        return True
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        return False
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return False

def main():
    """Main function"""
    print("Chinese Rap & Hip-Hop Song Filter Script")
    print("=" * 50)
    
    # Define file paths
    input_file = "chinese_songs.csv"
    output_file = "chinese_raphiphop.csv"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found")
        print("Please make sure the file exists in the current directory")
        return False
    
    # Filter rap and hip-hop songs
    success = filter_rap_hiphop_songs(input_file, output_file)
    
    if success:
        print(f"\n✅ Successfully filtered rap/hip-hop songs!")
        print(f"📁 Output file: {output_file}")
        
        # Display file size info
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"📊 Output file size: {file_size:,} bytes")
            
            # Count lines in output file
            with open(output_file, 'r', encoding='utf-8') as f:
                line_count = sum(1 for line in f)
            print(f"📈 Number of songs: {line_count - 1}")  # Subtract 1 for header
    else:
        print("\n❌ Failed to filter rap/hip-hop songs")
        return False
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

