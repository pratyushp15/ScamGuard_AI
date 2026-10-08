---
name: run-new-codebase
description: 'Use when entering an unfamiliar repository and asked to run, launch, or start its project. Identify the correct entry point, check prerequisites, start the appropriate app or command, and verify that it is running.'
argument-hint: 'Optional: name the app, service, or run target to launch'
---

# Run a Project in a New Codebase

Get an unfamiliar project to its normal runnable state with the smallest safe set of actions. Do not treat “run the project” as permission to change application behavior, perform destructive operations, or incur external costs.

## Workflow

1. **Orient to the repository.** Confirm the workspace root and read applicable `AGENTS.md`, `copilot-instructions.md`, or other repository instructions. Check the README and the nearest project manifest, task configuration, and documented launch instructions. Inspect only the entry-point files needed to resolve the run command.

2. **Choose the run target.** Prefer an explicit documented command or existing workspace task. Cross-check it against the project manifest and entry point. If the repository has multiple distinct runnable targets and the request does not identify one, ask which target to launch. Do not infer a run command from a filename alone or substitute a test, evaluation, migration, or data-processing command for the application.

3. **Check prerequisites.** Identify the required runtime and package manager from project configuration, then check their availability and whether the project environment is already prepared. Use the existing virtual environment or installed dependencies when suitable. If dependencies declared by the project are missing, install them with its package manager and lockfile without asking first, upgrading packages, or rewriting dependency versions. Check only whether required environment-variable names are documented or present; never display secret values. Do not invent credentials or make paid/external API calls as a startup probe.

4. **Resolve startup blockers carefully.** Use the first concrete error to identify the smallest next check. If setup instructions conflict with configuration, prefer an explicit project task or manifest and explain the conflict. Ask before changing source behavior, deleting or overwriting data, running migrations, escalating privileges, or taking an action that could incur cost. If a required secret or user choice is missing, stop at that boundary and state exactly what is needed.

5. **Launch the project.** Run the selected command from the repository root, using the project's configured environment. Keep foreground commands foreground; leave a process running only when it is a server or other intended long-running service. For interactive commands, do not submit sample input that could trigger external actions unless that is clearly safe and requested.

6. **Verify and report.** Confirm a concrete ready signal: for example, a server's local URL and successful response, a UI page loading, or a CLI reaching its expected prompt and completing a harmless check. Report the command used, the verification performed, any local URL, and remaining prerequisites or blockers. Do not claim success based only on a process starting if the application did not reach a usable state.

## Completion Criteria

- The run target and command are grounded in repository instructions or configuration.
- Required local prerequisites are satisfied, or the missing prerequisite is clearly identified.
- The application reaches a usable ready state without unintended data changes or external costs.
- The user receives the launch command, verification result, URL when applicable, and any remaining blocker.