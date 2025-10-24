#!/usr/bin/env python3
"""
Claude Code Hook Handler
=============================================
This script handles events from Claude Code and plays sounds for different actions.
It demonstrates event-driven programming and pattern matching in Python.

Cross-platform support: Windows, macOS, and Linux

Sound format selection:
    - Windows: Uses WAV files from sounds/wav/ (PowerShell SoundPlayer)
    - macOS: Uses MP3 files from sounds/mp3/ (afplay)
    - Linux: Uses MP3 files from sounds/mp3/ (mpg123, ffplay, paplay, or aplay)

Requirements: None (uses platform-native commands, no external dependencies)

Credit: Greg Baugues at https://www.haihai.ai/hooks/ for the initial codebase.
"""

import sys
import json
from pathlib import Path
import re
import platform
import subprocess

# ===== SOUND MAPPINGS =====
# This dictionary maps Claude Code events and tools to sound files
SOUND_MAP = {
    # System events - when Claude starts/stops
    "Notification": "notify",    # Claude is ready to help

    "Stop": "ready",           # Task completed
    "SubagentStop": "ready",   # Subtask completed

    # File editing tools - all use the same "edit" sound
    "Edit": "edit",            # Single file edit
    "MultiEdit": "edit",       # Multiple edits in one file
    "Write": "edit",           # Write new file
    "NotebookEdit": "edit",    # Edit Jupyter notebook

    # Task management
    "TodoWrite": "list",       # Update todo list

    # Read files
    "Read": "read",            # Read file content
    "NotebookRead": "read",    # Read Jupyter notebook

    # Bash command patterns - matched using regular expressions
    # Format: (regex_pattern, sound_name)
    "bash_patterns": [
        (r'^git commit', "commit"),                              # Git commits
        (r'^gh pr', "pr"),                                      # GitHub pull requests
        (r'^bundle exec rspec|^rspec|^bin/rspec', "test"),     # Ruby tests
        (r'^npm test|^yarn test|^pytest|^go test', "test"),    # Various test runners
        (r'.*', "bash"),  # Fallback: play "bash" sound for any unmatched Bash command
        # Add your own patterns here!
    ]
}

def play_sound(sound_name):
    """
    Play a sound file using platform-native commands.
    Cross-platform: Windows, macOS, Linux

    Windows uses WAV files (sounds/wav/)
    macOS and Linux use MP3 files (sounds/mp3/)

    Args:
        sound_name: Name of the sound file (without extension)

    Returns:
        True if sound played successfully, False otherwise
    """
    # Security check: Prevent directory traversal attacks
    if "/" in sound_name or "\\" in sound_name or ".." in sound_name:
        print(f"Invalid sound name: {sound_name}", file=sys.stderr)
        return False

    # Detect OS and select appropriate format
    system = platform.system()
    script_dir = Path(__file__).parent

    if system == "Windows":
        # Windows: use WAV files
        sounds_dir = script_dir / "sounds" / "wav"
        extension = ".wav"
    else:
        # macOS and Linux: use MP3 files
        sounds_dir = script_dir / "sounds" / "mp3"
        extension = ".mp3"

    # Build the path to the sound file
    file_path = sounds_dir / f"{sound_name}{extension}"

    if file_path.exists():
        try:
            if system == "Darwin":  # macOS
                subprocess.Popen(
                    ["afplay", str(file_path)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            elif system == "Windows":
                # Use PowerShell SoundPlayer for WAV files
                subprocess.Popen(
                    ["powershell", "-c",
                     f"(New-Object Media.SoundPlayer '{file_path}').PlaySync()"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            elif system == "Linux":
                # Try common Linux audio players
                for player in ["mpg123", "ffplay", "paplay", "aplay"]:
                    try:
                        subprocess.Popen(
                            [player, str(file_path)],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                        break
                    except FileNotFoundError:
                        continue

            return True

        except Exception as e:
            # Log error but don't crash
            print(f"Error playing sound {file_path.name}: {e}", file=sys.stderr)
            return False

    # Sound not found - fail silently to avoid disrupting Claude's work
    print(f"Sound file not found: {file_path}", file=sys.stderr)
    return False

def log_hook_data(hook_data):
    """
    Log the full hook_data to hook_handler.log for debugging/auditing.
    """
    try:
        log_path = Path(__file__).parent / "hook_handler.jsonl"
        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write(json.dumps(hook_data, ensure_ascii=False, indent=2) + "\n")
    except Exception as e:
        # Fail silently, but print to stderr for visibility
        print(f"Failed to log hook_data: {e}", file=sys.stderr)


def get_sound_for_event(hook_data):
    """
    Determine which sound to play based on Claude's action.

    Args:
        hook_data: Dictionary containing event information from Claude

    Returns:
        Sound name (string) or None if no sound should play
    """

    event_name = hook_data.get("hook_event_name", "")  # e.g., "Notification", "PreToolUse"
    tool_name = hook_data.get("tool_name", "")          # e.g., "Edit", "Bash", "TodoWrite"

    # Step 1: Check if this is a system event (like Claude starting up)
    if event_name in SOUND_MAP:
        return SOUND_MAP[event_name]

    # Step 2: Check if this is a known tool (like Edit or TodoWrite)
    if tool_name in SOUND_MAP:
        return SOUND_MAP[tool_name]

    # Step 3: Special handling for Bash commands
    # We look at the actual command to decide which sound to play
    if tool_name == "Bash" and event_name == "PreToolUse":
        # Get the actual bash command Claude is about to run
        command = hook_data.get("tool_input", {}).get("command", "")

        # Check each pattern to see if it matches the command
        for regex_pattern, sound_name in SOUND_MAP["bash_patterns"]:
            if re.match(regex_pattern, command, re.IGNORECASE):
                return sound_name

    # Step 4: No matching sound found
    return None

def main():
    """
    Main program - this runs when Claude triggers a hook.

    How it works:
    1. Claude sends event data as JSON through stdin
    2. We parse the JSON to understand what Claude is doing
    3. We decide which sound to play (if any)
    4. We play the sound and exit
    """
    ENABLE_LOG = False
    try:
        # Step 1: Read the event data from Claude
        # Claude sends JSON data through stdin (standard input)
        input_data = json.load(sys.stdin)
        if (ENABLE_LOG):
            log_hook_data(input_data)

        # Step 2: Figure out which sound to play
        sound_name = get_sound_for_event(input_data)

        # Step 3: Play the sound (if we found one)
        if sound_name:
            play_sound(sound_name)

        # Step 4: Exit successfully
        # Important: We always exit with code 0 (success) so we don't
        # interrupt Claude's work, even if something went wrong
        sys.exit(0)

    except json.JSONDecodeError as e:
        # Handle case where Claude sent invalid JSON
        print(f"Error parsing JSON input: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        # Handle any other unexpected errors
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


# ===== EXAMPLE EVENT DATA FROM CLAUDE =====
# Here's what Claude sends us for different events:
#
# When editing a file:
# {
#   "hook_event_name": "PreToolUse",
#   "tool_name": "Edit",
#   "tool_input": {
#     "file_path": "/path/to/file.py",
#     "old_string": "old code",
#     "new_string": "new code"
#   }
# }
#
# When running a bash command:
# {
#   "hook_event_name": "PreToolUse",
#   "tool_name": "Bash",
#   "tool_input": {
#     "command": "git commit -m 'Update feature'"
#   }
# }
#
# When Claude is ready:
# {
#   "hook_event_name": "Notification"
# }


# Entry point - Python calls main() when the script runs
if __name__ == "__main__":
    main()