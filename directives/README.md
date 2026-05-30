# Layer 1: Directives (Standard Operating Procedures)

This directory contains natural language SOPs (Standard Operating Procedures) that outline user intents, workflow goals, expectations, constraints, and inputs/outputs.

Directives act as the instructions given to a mid-level employee. The orchestration agent (Layer 2) reads these instructions to make intelligent routing decisions and coordinates with Layer 3 deterministic Python scripts to carry them out.

## Directive File Template

Every new directive should follow this structure to remain consistent:

```markdown
# [Directive Name]

## Goal
A clear, concise statement of what this directive achieves.

## Inputs
Required and optional inputs, variables, parameters, or configurations.

## Steps (Workflow)
1. **Analyze:** Check inputs, logs, or existing status.
2. **Execute:** Specific deterministic tool scripts in `execution/` to run (and the order to run them).
3. **Handle Errors:** What to do when scripts fail (retry, check credentials, fall back, alert).
4. **Output / Deliverables:** Where the results go (Google Sheets, Slides, local files, Slack, etc.).

## Constraints & Edge Cases
- Rate limits
- Missing API keys
- Validation expectations

## Verification
- How to verify that this directive succeeded.
```

## Creating New Directives
- **Don't create directives extemporaneously**: Only create directives when designing reusable processes.
- **Improve incrementally**: When you encounter API rate limits, schema deviations, or specific errors during execution, update the relevant directive immediately to self-anneal the agent's behavior.
