# Review Pull Request

Review PR #$ARGUMENTS (or the current branch's PR if no number provided).

## Instructions

1. **Fetch PR Information**
   - If a PR number is provided, use `gh pr view $ARGUMENTS` to get PR details
   - If no PR number, use `gh pr view` for the current branch's PR
   - Get the PR diff with `gh pr diff`

2. **Analyze the Changes**
   Review the code for:
   - **Correctness**: Does the code do what it's supposed to do?
   - **Security**: Any potential vulnerabilities (injection, XSS, auth issues)?
   - **Performance**: Inefficient algorithms, N+1 queries, memory leaks?
   - **Code Quality**: Readability, maintainability, follows project conventions?
   - **Testing**: Are there adequate tests? Are edge cases covered?
   - **Documentation**: Are public APIs documented? Are complex sections explained?

3. **Provide Structured Feedback**
   Format your review as:

   ### Summary
   Brief overview of what the PR does and overall assessment.

   ### Highlights
   What's done well.

   ### Issues
   Problems that should be addressed, categorized by severity:
   - **Critical**: Must fix before merge (security, data loss, breaking changes)
   - **Major**: Should fix (bugs, performance issues)
   - **Minor**: Nice to fix (style, minor improvements)

   ### Suggestions
   Optional improvements that aren't blocking.

   ### Verdict
   One of: **Approve**, **Request Changes**, or **Comment**

4. **Check CI Status** (optional)
   Use `gh pr checks` to see if CI is passing.
