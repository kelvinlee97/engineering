# Using Codex IDE Context in VS Code

Chinese version: [README_ZH.md](README_ZH.md)

This guide explains how to connect Codex to VS Code's IDE context and use that context effectively while working in a repository. It is written for VS Code only.

OpenAI states that the Codex VS Code extension also works with most VS Code forks; this guide intentionally does not document their different menus or setup flows. See the official [Codex IDE extension guide](https://developers.openai.com/codex/ide) for the supported sidebar and editor-context workflow.

## What IDE context adds

When you attach editor context to the Codex composer, Codex can use it as extra task context. Depending on the extension version and configuration, this can include the current file, selected code, cursor-adjacent code, and editor diagnostics.

It is an aid, not a replacement for repository inspection:

- Codex still reads relevant files and runs checks when the task needs evidence beyond the editor.
- It does not mean that the entire repository has been automatically read.
- It does not grant permission to commit, push, deploy, delete files, or change external systems.

## Connect IDE context

1. In VS Code, open the repository with **File > Open Folder...**. Open the folder, not only an individual file.
2. If VS Code shows **Restricted Mode**, first review the folder and confirm that you trust its source. Only then select **Manage** and trust the workspace. If the banner is not visible, open the Command Palette (`Cmd+Shift+P` on macOS) and run **Workspaces: Manage Workspace Trust**. Then run **Developer: Reload Window**.
3. Open Extensions (`Cmd+Shift+X`), locate the Codex extension, and ensure that it is enabled. Apply an available update and reload VS Code if prompted.
4. Open the Codex sidebar by selecting the Codex icon. If the icon is not visible, open the Command Palette and run **Codex: Open Codex Sidebar**.
5. Open a source file and select the code or text relevant to your task. In the Codex composer, add the current file or selection as context, then send your task.
6. Verify the attached context with a small request such as:

   ```text
   Tell me the current file path and summarize the selected code.
   ```

If the result correctly reflects the file or selection attached to the composer, that editor context was included with the request.

## Use it in daily work

Open the relevant file, select the smallest useful block, add the file or selection to the Codex composer, and give Codex a task with an expected outcome. For example:

```text
Explain this code and identify its edge cases.
```

```text
Diagnose the current editor error, explain the root cause, make the smallest safe fix, and run the relevant verification.
```

```text
Refactor this selected logic for clarity without changing its public behavior. Add or update focused tests.
```

```text
Review this API handler for authorization, validation, and error-handling issues. Do not modify it yet.
```

For a cross-file task, say so explicitly. If the current session has workspace read access, Codex can use the selected code as its starting point and then search the repository for callers, types, configuration, and tests. IDE context itself does not grant that access.

## Troubleshooting

If you cannot open the Codex sidebar or attach editor context, work through these steps in order:

1. Confirm that the prompt is in the Codex panel inside the VS Code window where the repository folder is open.
2. If the workspace is in Restricted Mode, review the folder and confirm that you trust its source before trusting it. Use the **Manage** link or run **Workspaces: Manage Workspace Trust** from the Command Palette, then reload the window.
3. Confirm that the Codex extension is enabled and does not show **Reload Required**.
4. Open a real project file, select a few lines, add the file or selection to the composer, and send a small test request.
5. Start a new Codex conversation and try attaching the file or selection again.
6. Update the Codex extension. If the problem persists, uninstall it, fully restart VS Code, reinstall it, reopen the trusted workspace, open the Codex sidebar, and retry attaching the context.

If IDE context remains unavailable, provide a repository-relative file path, the selected code, or the exact diagnostic in your prompt. If the current session has workspace read access, Codex can still inspect relevant repository files and work from that explicit context.

## Version and privacy notes

The available IDE context and composer controls can change with the Codex extension version, VS Code configuration, and workspace policy. Treat the context attached and displayed by your installed client as the source of truth for the current request. For VS Code's trust behavior and Restricted Mode, see the official [Workspace Trust documentation](https://code.visualstudio.com/docs/editing/workspaces/workspace-trust).

Do not paste credentials, access tokens, private keys, production data, or employer/client-confidential material into a prompt or a public repository issue. Follow your organization’s workspace and data-handling policies when using local development tools.
