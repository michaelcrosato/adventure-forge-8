# Process v1

Serial factory. One builder task at a time. Orchestrator writes the kernel. Subagents wait.

1. Assess gaps against PLAN.md.
2. Do the next slice or fix.
3. Record traces.
4. Run `python -m adventure_forge verify`.
5. Push if green.

This file is not sacred. Honesty is.
