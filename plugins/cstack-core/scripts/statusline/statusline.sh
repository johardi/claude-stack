#!/bin/bash
# statusline.sh — Claude Code status line for cstack-core
# Displays git branch, model info, token counts, and context window usage.

# Read JSON from stdin (Claude pipes session data here).
INPUT=$(cat)

# --- Git branch (from workspace.current_dir if available, else cwd) ---
BRANCH=""
if command -v jq >/dev/null 2>&1; then
  WORK_DIR=$(printf '%s' "$INPUT" | jq -r '.workspace.current_dir // .cwd // empty' 2>/dev/null)
fi
WORK_DIR="${WORK_DIR:-$PWD}"
if command -v git >/dev/null 2>&1 && [ -n "$WORK_DIR" ]; then
  BRANCH=$(git -C "$WORK_DIR" --no-optional-locks rev-parse --abbrev-ref HEAD 2>/dev/null)
fi

# --- Model name + effort ---
MODEL_LABEL=""
if command -v jq >/dev/null 2>&1; then
  MODEL_NAME=$(printf '%s' "$INPUT" | jq -r '.model.display_name // empty' 2>/dev/null)
  THINKING=$(printf '%s' "$INPUT" | jq -r '.session.thinking_enabled // empty' 2>/dev/null)
  if [ -n "$MODEL_NAME" ]; then
    MODEL_LABEL="$MODEL_NAME"
    if [ "$THINKING" = "true" ]; then
      MODEL_LABEL="$MODEL_LABEL (thinking)"
    fi
  fi
fi

# --- Token counts ---
TOKEN_LABEL=""
if command -v jq >/dev/null 2>&1; then
  IN_RAW=$(printf '%s' "$INPUT" | jq -r '.context_window.current_usage.input_tokens // .context_window.total_input_tokens // empty' 2>/dev/null)
  OUT_RAW=$(printf '%s' "$INPUT" | jq -r '.context_window.current_usage.output_tokens // .context_window.total_output_tokens // empty' 2>/dev/null)

  # Format a raw number as e.g. 1.2k or 45k or 123
  fmt_num() {
    local n="$1"
    if [ -z "$n" ] || [ "$n" = "null" ]; then echo "0"; return; fi
    if [ "$n" -ge 1000 ] 2>/dev/null; then
      awk -v n="$n" 'BEGIN { x=n/1000; printf (x==int(x)) ? "%dk" : "%.1fk", x }'
    else
      echo "$n"
    fi
  }

  IN_FMT=$(fmt_num "$IN_RAW")
  OUT_FMT=$(fmt_num "$OUT_RAW")
  if [ -n "$IN_RAW" ] || [ -n "$OUT_RAW" ]; then
    TOKEN_LABEL="↓${IN_FMT} ↑${OUT_FMT}"
  fi
fi

# --- Context window usage % ---
CTX_LABEL=""
if command -v jq >/dev/null 2>&1; then
  CTX_PCT=$(printf '%s' "$INPUT" | jq -r '.context_window.used_percentage // empty' 2>/dev/null)
  if [ -n "$CTX_PCT" ] && [ "$CTX_PCT" != "null" ]; then
    CTX_INT=$(printf '%.0f' "$CTX_PCT" 2>/dev/null)
    CTX_LABEL="ctx:${CTX_INT}%"
  fi
fi

# --- Assemble output ---
# Parts are joined with " | " separator; empty parts are skipped.
PARTS=()
[ -n "$WORK_DIR" ]    && PARTS+=("📁 ${WORK_DIR/#$HOME/~}")
[ -n "$BRANCH" ]      && PARTS+=("⎇ $BRANCH")
[ -n "$MODEL_LABEL" ] && PARTS+=("⚡ $MODEL_LABEL")
[ -n "$TOKEN_LABEL" ] && PARTS+=("$TOKEN_LABEL")
[ -n "$CTX_LABEL" ]   && PARTS+=("📊 $CTX_LABEL")

# Join with separator
RESULT=""
for PART in "${PARTS[@]}"; do
  if [ -z "$RESULT" ]; then
    RESULT="$PART"
  else
    RESULT="$RESULT | $PART"
  fi
done

printf '%s' "$RESULT"
