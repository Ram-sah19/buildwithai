# Layer 3: Execution (Deterministic Tools)

This directory contains deterministic Python scripts that do the actual work. They process data, call APIs, manipulate the filesystem, or interact with databases. 

By separating business logic and API execution into structured Python scripts, we ensure that:
1. Operations are repeatable, fast, and testable.
2. The AI client handles only high-level decision routing and error recovery, reducing cascading model errors.

## Design Rules for Execution Scripts

When writing Python scripts in this directory, always adhere to the following rules:

1. **Standalone Execution:** Ensure scripts can be run directly from the command line using standard command line arguments (e.g. using `argparse`).
2. **Explicit Error Handling:** Avoid silent failures. Catch and raise descriptive exceptions, print informative tracebacks, and use appropriate exit codes.
3. **Structured Outputs:** When writing outputs, prefer standard file structures (e.g. CSV, JSON, Markdown) in `tmp/` or cloud formats.
4. **Environment Variables:** Never hardcode credentials. Load API keys, tokens, and database links from environment variables using `dotenv` or `os.environ`.
5. **Robust Logging:** Log execution steps to standard output or stderr to assist in debugging and orchestrator diagnostics.
