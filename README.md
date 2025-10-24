# Claude Stack

A curated collection of Claude Code plugins providing specialized agents, commands, and development tools to enhance your coding workflow with AI assistance.

## Overview

Claude Stack is a modular plugin ecosystem designed to supercharge your development experience with Claude Code. It offers domain-specific expert agents, automation tools, audio feedback hooks, and integrated MCP servers to maintain consistency and boost productivity across your projects.

**Created by**: Josef Hardi ([@johardi](https://github.com/johardi))

## Features

- **Specialized AI Agents**: Expert agents for debugging, web development, cloud architecture, Python, Java, and GitHub Actions
- **Slash Commands**: Quick access to onboarding workflows and GitHub issue analysis
- **Audio Feedback**: Cross-platform sound notifications for Claude Code events (tool use, completions, etc.)
- **MCP Integration**: Built-in Serena and Context7 MCP servers for enhanced IDE capabilities
- **Modular Design**: Install only what you need - pick from web, Python, Java, or essential bundles

## Plugins

### cstack-essential

**Essential development bundle** - Core tools for any development workflow.

**Features**:
- **Slash Commands**:
  - `/onboard` - Comprehensive codebase onboarding with exploration and documentation
  - `/issue` - Automated GitHub issue analysis, branching, fixing, and PR creation
- **Agents**:
  - `debugger` - Root cause analysis for runtime errors, test failures, and performance issues
  - `github-actions-specialist` - CI/CD pipeline design and workflow optimization
- **Audio Notifications**: Cross-platform sound feedback for Claude events (macOS/Linux: MP3, Windows: WAV)
- **MCP Servers**:
  - Serena - Advanced IDE assistant with code navigation and analysis
  - Context7 - Contextual code understanding via Upstash

**Hooks Configuration**:
- `Notification` - Sound when Claude is ready
- `Stop` / `SubagentStop` - Sound on task completion
- `PreToolUse` - Sounds for Edit, Write, Bash, TodoWrite, etc.

### cstack-web

**Web development bundle** - Expert agents for modern web applications.

**Agents**:
- `frontend-developer` - React 19+, Next.js 15+, TypeScript, Tailwind, accessibility, Core Web Vitals
- `cloud-architect` - Multi-cloud (AWS/Azure/GCP), IaC (Terraform/CDK), Kubernetes, FinOps, security

**Use Cases**:
- Building React/Next.js applications with server components
- Designing scalable cloud infrastructure
- Performance optimization and SEO
- Multi-region deployments and disaster recovery

### cstack-python

**Python development bundle** - Modern Python 3.12+ expertise.

**Agents**:
- `python-pro` - FastAPI/Django, async/await, type hints, modern tooling (uv/ruff/mypy), pytest

**Use Cases**:
- FastAPI/Django REST APIs
- Async data pipelines
- Performance optimization
- Production-ready Python applications

### cstack-java

**Java development bundle** - Enterprise Java 18+ expertise.

**Agents**:
- `java-pro` - Spring Boot 3.x, virtual threads, microservices, JPA/Hibernate, testing

**Use Cases**:
- Spring Boot microservices
- Enterprise application development
- JVM performance tuning
- Cloud-native Java applications

## Installation

### Prerequisites

- [Claude Code](https://claude.com/claude-code) installed
- Python 3.x (for audio hooks in cstack-essential)
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
   - **cstack-essential** - Core development tools with audio feedback
   - **cstack-web** - React/Next.js and cloud architecture experts
   - **cstack-python** - Python 3.12+ development expertise
   - **cstack-java** - Java 18+ and Spring Boot experts

2. Select the plugin(s) you want to install
3. Choose **"Install now"**
4. Restart Claude Code when prompted

#### Step 3: Verify Installation

Type `/help` in Claude Code to verify that new commands are available. For example, if you installed `cstack-essential`, you should see:
- `/onboard` - Comprehensive codebase onboarding
- `/issue` - GitHub issue analysis and fixing

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
    "cstack-essential@claude-stack",
    "cstack-web@claude-stack"
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

### Using Slash Commands

```bash
# Onboard to a new codebase
/onboard [optional context about the project]

# Analyze and fix a GitHub issue
/issue #123
```

### Invoking Agents

Agents are automatically invoked based on context, or you can explicitly request them:

```
"Use the debugger agent to find why my tests are failing"
"Use frontend-developer to optimize this React component"
"Use cloud-architect to design the AWS infrastructure"
```

### Audio Notifications

The cstack-essential plugin includes audio feedback for various Claude Code events:

- **Notification**: Claude is ready
- **Edit/Write/Read**: File operations
- **Bash**: Command execution (with special sounds for git, tests, PRs)
- **TodoWrite**: Task list updates
- **Stop**: Task completion

#### Troubleshooting Audio

If you're not hearing sounds:

1. **Verify Python Installation**:
   ```bash
   python3 --version
   ```

2. **Check Sound Files**:
   ```bash
   ls plugins/cstack-essential/scripts/play-sound/sounds/mp3/
   # macOS/Linux should have MP3 files
   ls plugins/cstack-essential/scripts/play-sound/sounds/wav/
   # Windows should have WAV files
   ```

3. **Test Sound Playback Manually**:
   ```bash
   # macOS
   afplay plugins/cstack-essential/scripts/play-sound/sounds/mp3/notify.mp3

   # Linux (requires mpg123 or similar)
   mpg123 plugins/cstack-essential/scripts/play-sound/sounds/mp3/notify.mp3

   # Windows (PowerShell)
   (New-Object Media.SoundPlayer 'plugins/cstack-essential/scripts/play-sound/sounds/wav/notify.wav').PlaySync()
   ```

4. **Enable Debug Logging**:
   Edit `plugins/cstack-essential/scripts/play-sound/play_sound.py` and set:
   ```python
   ENABLE_LOG = True  # Line 195
   ```
   Then check `plugins/cstack-essential/scripts/play-sound/hook_handler.jsonl` for debug output.

5. **Verify Hook Configuration**:
   Check that hooks are properly configured in `.claude-plugin/marketplace.json`


## License

MIT License - see LICENSE file for details.

## Credits

- Audio hook implementation inspired by [Greg Baugues](https://www.haihai.ai/hooks/)
- Built for [Claude Code](https://claude.com/claude-code) by Anthropic

## Support

For issues, questions, or contributions:
- GitHub Issues: [https://github.com/johardi/claude-stack/issues](https://github.com/johardi/claude-stack/issues)

---

**Note**: This is a personal plugin collection. Feel free to fork and customize for your own needs!
