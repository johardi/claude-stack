# Claude Stack

A curated collection of Claude Code plugins providing specialized skills, hooks, and MCP integrations to enhance your coding workflow with AI assistance.

## Overview

Claude Stack is a modular plugin ecosystem designed to supercharge your development experience with Claude Code. It offers workflow automation, audio feedback hooks, and integrated MCP servers to maintain consistency and boost productivity across your projects.

**Created by**: Josef Hardi ([@johardi](https://github.com/johardi))

## Plugins

### cstack-core

**Essential development bundle** - Core tools for any development workflow.

**Skills**:
- `github-issue-workflow` - Structured 8-phase workflow for resolving GitHub issues: fetch details, analyze requirements, implement, verify, review, commit, and create PRs
- `karpathy-guidelines` - Behavioral guidelines to reduce common LLM coding mistakes: think before coding, simplicity first, surgical changes, and goal-driven execution

**Audio Notifications**: Cross-platform sound feedback for Claude Code events (macOS/Linux: MP3, Windows: WAV)

**Hooks**:
- `Notification` - Sound when Claude is ready
- `Stop` / `SubagentStop` - Sound on task completion
- `PreToolUse` - Sounds for Edit, Write, Bash, TodoWrite, etc.

**MCP Servers**:
- [Serena](https://github.com/oraios/serena) - Advanced IDE assistant with code navigation and analysis
- [ref-tools-mcp](https://www.npmjs.com/package/ref-tools-mcp) - Library and framework documentation search

### cstack-collab

**Multi-agent collaboration patterns** - Coordinate a parent GitHub issue that has been broken into dependent sub-tickets, with one PR per sub-ticket and human-in-the-loop merge gates. Pairs an upfront authoring skill with a runtime orchestrator.

**Skills**:
- `compose-tickets` - Turn a feature description into a structured parent issue plus standardized sub-tickets that `orchestrate-tickets` can execute directly. Two confirmation gates (decomposition, drafts) and a deterministic linter before filing.
- `orchestrate-tickets` - Execute a parent's sub-tickets by spawning per-ticket workers in isolated git worktrees. Builds a dependency DAG from `Depends on #N` markers, runs independent tickets in parallel, serializes dependents, and yields to the user between waves for review/merge. Never auto-merges.

**Scripts** (deterministic helpers the skills delegate to):

| Script | Purpose |
|--------|---------|
| `state.py` | CRUD over `.cstack-collab/state.json` — the active orchestration state file (parent, waves, per-child PR/branch/merged) |
| `check-prereqs.sh` | gh/git preflight + default-branch detection; stable exit codes |
| `build-dag.py` | Construct execution DAG from `Depends on #N` markers; refuses cycles |
| `wave-status.py` | Poll PR merge state across a wave; rolls a single exit code |
| `update-parent-checklist.py` | Idempotent parent-issue checklist toggler with a marker comment |
| `worker-prompt.sh` | Render the worker contract template (single source of truth) |
| `lint-ticket.py` | Validate a compose-tickets body before `gh issue create` (catches the prose-vs-marker bug) |

**Hooks** (all scope-aware: no-op outside an active orchestration):

| Hook | Enforces |
|------|----------|
| `deny-merge` | Refuses `gh pr merge` against any child PR while orchestration is active |
| `deny-parent-mutations` | Refuses `gh issue close <PARENT>` while children unmerged; refuses parent body rewrites without the cstack-collab marker |
| `record-worker` | PostToolUse(Agent) — parses worker JSON returns and updates state.json automatically |
| `session-start-summary` | Surfaces in-progress orchestrations on session start so cold-resumes pick up the right wave |

**Escape hatch**: set `CSTACK_COLLAB_OVERRIDE=1` in the env to bypass any single deny hook with a loud stderr warning.

### cstack-guardrails

**Always-on git/gh hygiene** - Three PreToolUse(Bash) hooks that protect the default branch and discourage skipping pre-commit hooks. Independent of cstack-collab; install either, both, or neither.

**Hooks**:

| Hook | Enforces |
|------|----------|
| `deny-no-verify` | Refuses `--no-verify`, `--no-gpg-sign`, and `commit.gpgsign=false` on git/gh commands |
| `deny-force-push-default` | Refuses `git push --force` (or `-f` / `--force-with-lease`) to the default branch |
| `deny-commit-on-default` | Refuses `git commit` while on the default branch (encourages branch-per-feature) |

Default branch is detected via `gh repo view`, falling back to `origin/HEAD`. Each hook honors `CSTACK_GUARDRAILS_OVERRIDE=1` for emergency bypass with a loud stderr warning.

## Installation

### Prerequisites

- [Claude Code](https://claude.com/claude-code) installed
- Python 3.x (for audio hooks in cstack-core)
- Git (for version control integration)

### Installing Plugins

Claude Stack plugins are distributed through the Claude Code Marketplace system. All installation is done interactively through Claude Code.

#### Step 1: Add the Claude Stack Marketplace

In Claude Code, type `/plugin` and select **"Add marketplace"**, then:

1. Enter the GitHub repository: `johardi/claude-stack`
2. Confirm to add the marketplace

#### Step 2: Install Desired Plugins

In Claude Code, type `/plugin` and select **"Browse Plugins"**, then:

1. Browse the available plugins:
   - **cstack-core** - Core development tools with audio feedback and MCP servers
   - **cstack-collab** - Multi-agent orchestration with worktree-isolated workers and human-in-the-loop merge gates
   - **cstack-guardrails** - Always-on git/gh hygiene hooks (no-verify, force-push to main, commit on main)

2. Select the plugin(s) you want to install
3. Choose **"Install now"**
4. Restart Claude Code when prompted

#### Step 3: Verify Installation

Type `/help` in Claude Code to verify that new skills are available.

#### Team/Repository Setup (Optional)

For team-wide plugin distribution, add this to your repository's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "claude-stack": {
      "source": {
        "source": "github",
        "repo": "johardi/claude-stack"
      }
    }
  },
  "plugins": [
    "cstack-core@claude-stack"
  ]
}
```

When team members trust the folder, they'll automatically get the marketplace and plugins configured.

#### Managing Plugins

Use `/plugin` in Claude Code to access plugin management:
- **Update marketplace** - Refresh to get latest plugin versions
- **Enable/Disable** - Toggle plugins without uninstalling
- **Uninstall** - Remove plugins completely

## Usage

### Using Skills

Skills are automatically activated based on task context. For example, when you reference a GitHub issue:

```
"Fix issue #123"
"Resolve the bug reported in #456"
```

The `github-issue-workflow` skill activates and guides you through the 8-phase resolution process.

### Audio Notifications

The cstack-core plugin includes audio feedback for various Claude Code events:

- **Notification**: Claude is ready
- **Edit/Write**: File operations
- **Bash**: Command execution
- **TodoWrite**: Task list updates
- **Stop**: Task completion

#### Troubleshooting Audio

If you're not hearing sounds:

1. **Verify Python Installation**:
   ```bash
   python3 --version
   ```

2. **Test Sound Playback Manually**:
   ```bash
   # macOS
   afplay plugins/cstack-core/scripts/play-sound/sounds/mp3/notify.mp3

   # Linux (requires mpg123 or similar)
   mpg123 plugins/cstack-core/scripts/play-sound/sounds/mp3/notify.mp3

   # Windows (PowerShell)
   (New-Object Media.SoundPlayer 'plugins/cstack-core/scripts/play-sound/sounds/wav/notify.wav').PlaySync()
   ```

3. **Enable Debug Logging**:
   Edit `plugins/cstack-core/scripts/play-sound/play_sound.py` and set:
   ```python
   ENABLE_LOG = True  # Line 195
   ```
   Then check `plugins/cstack-core/scripts/play-sound/hook_handler.jsonl` for debug output.

## License

MIT License - see LICENSE file for details.

## Credits

- **karpathy-guidelines** skill by [Jiayuan Zhang](https://github.com/forrestchang) ([@forrestchang](https://github.com/forrestchang)), from [andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills)
- Audio hook implementation inspired by [Greg Baugues](https://www.haihai.ai/hooks/)
- Built for [Claude Code](https://claude.com/claude-code) by Anthropic

## Support

For issues, questions, or contributions:
- GitHub Issues: [https://github.com/johardi/claude-stack/issues](https://github.com/johardi/claude-stack/issues)

---

**Note**: This is a personal plugin collection. Feel free to fork and customize for your own needs!
