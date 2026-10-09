# ascii-media-dump

Recover unfinished ideas, understand the original vision, complete them as if they had continued to be actively developed, and publish them as polished, production-quality open-source repositories.

## Objective

NOT to upload old projects.

Recover unfinished ideas, understand the original vision, complete them as if they had continued to be actively developed, and publish them as polished, production-quality open-source repositories.

## Root Directory

D:\pedrive stuff\I MADE THIS\Learning & Experiments

## Important

Every immediate child folder inside the root directory represents an independent project.

DO NOT create one repository for the entire folder.

Create one GitHub repository per completed project.

Process projects sequentially.

Never mix code between projects.

Finish one repository completely before starting the next.

## Special Case

Project:

D:\pedrive stuff\I MADE THIS\Learning &Experiments\ascii-media-dump

This project contains multiple development stages.

Treat them as research material rather than separate repositories.

Project structure:

ASCII-generator-master
    Primary implementation.
    This is the base project.

importants
    Important experiments.
    Reuse useful ideas whenever appropriate.

try_2026
    Recent failed prototype.
    Analyze it carefully.
    Recover useful ideas.
    Merge successful concepts into the final project.
    Do not publish this folder independently.

The final repository should represent the best possible evolution of everything learned across these folders.

## Project Philosophy

Many projects are incomplete.

Many contain broken code.

Many contain only an experiment.

Many contain only an idea.

Do NOT simply polish them.

Understand what the original project was trying to become.

Then finish building it.

Think like the original developer returned after another year of full-time work.

Continue the project naturally.

Never replace the original concept.

Extend it.

## Engineering Standard

Do not stop because something works.

Continue improving until you cannot identify any meaningful engineering improvement.

Improve every reasonable aspect including:

• architecture
• algorithms
• code quality
• modularity
• maintainability
• readability
• UI
• UX
• accessibility
• responsiveness
• animations
• performance
• memory usage
• startup time
• developer experience
• logging
• configuration
• testing
• deployment
• CI/CD
• packaging
• documentation
• error handling
• validation
• security
• scalability
• portability
• repository organization
• naming
• consistency
• API design
• user workflow

When appropriate you may redesign significant portions of the project while preserving its purpose.

## Recover Missing Work

If features appear unfinished:

Complete them.

If modules are missing:

Implement them.

If placeholders exist:

Replace them.

If TODOs exist:

Finish them.

If mock data exists:

Replace it where appropriate.

If architecture is weak:

Redesign it.

If UI is basic:

Create a polished modern UI.

If the project deserves additional capabilities that naturally fit its purpose:

Implement them.

## Research

You may study modern implementations, papers, documentation, open-source repositories, and best practices to improve engineering quality.

Do NOT clone another project.

Do NOT copy copyrighted code.

Learn from existing work and build an original implementation appropriate for this repository.

## Audit

Produce a complete engineering audit before modifications.

Identify:

• strengths
• weaknesses
• technical debt
• duplicated code
• dead code
• missing modules
• broken architecture
• missing documentation
• missing tests
• security issues
• dependency issues
• performance issues
• portability issues
• maintainability issues

## Cleanup

Remove only unnecessary artifacts.

Never delete useful source code.

Generate or improve:

README.md
LICENSE
CHANGELOG.md
CONTRIBUTING.md
CODE_OF_CONDUCT.md
SECURITY.md
ROADMAP.md
TODO.md
.gitignore

README must accurately describe the final project, not the original prototype.

## Security

Before every commit and push:

• scan for secrets
• remove credentials
• remove .env files
• remove API keys
• remove machine-specific files
• remove caches
• remove build artifacts
• remove generated files
• verify .gitignore

If any secret is detected:

STOP.

Remove it.

Verify again.

Only continue after the repository is clean.

## Quality Gate

Do not declare a project finished until all of the following pass:

✓ builds successfully
✓ runs successfully
✓ runtime verified
✓ no obvious bugs
✓ documentation complete
✓ repository clean
✓ no secrets
✓ no unnecessary files
✓ coherent architecture
✓ production-quality repository layout

## GitHub

For each completed project:

1. Search my GitHub account (NotAzie) for an equivalent repository.

2. Compare by implementation similarity, not only repository name.

3. If a matching repository already exists:
   • update that repository
   • preserve existing Git history
   • push to the correct branch

4. If no matching repository exists:
   • create a new repository with a professional name
   • configure the remote
   • push only after all quality gates pass

Never create duplicate repositories for the same project.

## Final Release Gate

Before pushing:

Perform one final release audit.

Verify:

✓ application builds
✓ runtime verified
✓ documentation complete
✓ assets correct
✓ no duplicate files
✓ no dead code
✓ no broken links
✓ no secrets
✓ clean Git status

If any verification fails:

Fix it.

Repeat verification.

Do not push until every check passes.

## Commits

Group related work logically.

Use professional commit messages.

Do not create meaningless commits.

## Publish

Only after every verification succeeds:

• commit all remaining changes
• push to the correct GitHub repository under NotAzie
• verify the push succeeded
• verify the latest commit exists remotely
• verify local HEAD matches origin
• verify the working tree is clean

After a project is complete, automatically continue to the next project inside:

D:\pedrive stuff\I MADE THIS\Learning & Experiments

Continue until every project has been processed.
