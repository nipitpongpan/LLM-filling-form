#!/bin/bash

# Define source and destination directories
SOURCE_DIR="template"
DEST_DIR="result"

# remove all files in the destination path
rm "$DEST_DIR"/*

# Copy all files from the source directory to the destination directory
cp -r "$SOURCE_DIR"/* "$DEST_DIR"

mv "$DEST_DIR"/template.json "$DEST_DIR"/current.json 
