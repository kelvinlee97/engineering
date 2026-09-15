# Mermaid and Bilingual Quality

## Mermaid contract

Every Mermaid block must include a concise accessible title and description:

```mermaid
flowchart TD
    accTitle: Request path to a workload
    accDescr: A client request enters through the ingress, is routed by a service, and reaches one selected pod.
    Client --> Ingress
    Ingress --> Service
    Service --> Pod
```

- Use syntax supported by both GitHub and the repository's pinned Material for MkDocs version.
- Prefer flowchart, sequence, state, class, and entity-relationship diagrams for predictable site styling.
- Treat architecture, mind map, timeline, and experimental diagram types as requiring explicit mobile and theme verification.
- Do not embed secrets, private infrastructure identifiers, confidential names, or unsafe HTML.
- Do not use custom styling merely for decoration. Ensure meaning does not depend on colour alone.
- Keep a text interpretation next to each diagram so the essential meaning survives renderer or accessibility failure.

## Paired languages

English and Chinese diagrams must have the same factual topology:

- Keep node and edge meaning aligned.
- Translate reader-facing labels and accessibility text.
- Preserve commands, identifiers, API names, resource types, protocol names, and code where translation would reduce precision.
- A necessary label-length adaptation may change layout, but not scope or meaning.

## Validation

For any article containing Mermaid:

1. Confirm diagram count, type, and topology across both languages.
2. Confirm every block has `accTitle` and `accDescr`.
3. Run the knowledge-base validation and `mkdocs build --strict`.
4. Inspect the rendered article, not only the Markdown source.
5. Check a desktop and narrow mobile viewport for clipping, tiny labels, excessive height, and horizontal overflow.
6. Check light and dark themes when diagram or site styling changes.
7. Run `git diff --check` and verify local links.
