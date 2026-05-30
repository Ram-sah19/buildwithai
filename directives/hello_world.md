# Hello World Directive

## Goal
Generate a personalized greeting card/report as a markdown deliverable in the `tmp/` directory based on the user's name and optional title.

## Inputs
- `name` (required): The name of the user.
- `title` (optional): The title or role of the user (e.g. "Senior Developer", "Architect").

## Steps (Workflow)
1. **Validate Inputs:** Ensure a valid name is provided.
2. **Execute Execution Tool:** Run the script `execution/hello_world.py` with arguments `--name` and `--title` (if provided).
3. **Handle Errors:**
   - If missing name: exit with error code 1.
   - If system/environment validation fails: print descriptive error trace and self-anneal execution script config.
4. **Deliverable:**
   - Write a markdown report file to `tmp/greeting_<timestamp>.md`.
   - The orchestration layer will report the final path and summarize the message to the user.

## Constraints & Edge Cases
- Clean outputs only: the output report should not contain raw console debugging lines.
- Safe pathing: always write to the correct relative path `/tmp` within the project.

## Verification
- Verify the file is generated under `tmp/`.
- Read and verify the contents of the generated file match the provided input name.
