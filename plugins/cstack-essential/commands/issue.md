Please analyze and fix the GitHHub issue: $ARGUMENTS.

Follow these steps:

# Plan
1. Use `gh issue view` to get the issue details
2. Understand the problem described in the issue
3. Ask clarifying questions if needed
4. Understand the prior art of this issue
  - Search the scratchpads for previous thoughts related to the issue
  - Search PRs to see if you can find history on this issue
  - Search the codebase for relevant files
5. This harder about how to break the issue down into series of small, manageable tasks
6. Document your plan in a .claude/tasks/[ISSUE_ID]/scratchpad-[issue_name].md file.
  - Include the issue name in the filename
  - Include a link to the issue in the scratchpad

# Create
  - Create a new branch for the issue
  - Solve the issue in small, manageable steps, according to your plan
  - Commit your changes after each step.

# Test
  - Write unit tests to describe the expected behavior of your code
  - Run the full test suite to ensure you haven't broken anything
  - If the tests are failing, fix them
  - Ensure that all tests are passing before moving to the next step

# Deploy
  - Open a PR and request a review