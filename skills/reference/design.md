# Design — luca room multi-page specification

> This file defines the visual and interaction rules for the pages under `projects/room/`. It supports `skills/room.md` and keeps room output consistent across luca instances.

## Purpose

The room is a small operational site. `dashboard.html` is the overview and navigation entry; topic pages are focused workbenches.

It must help the user quickly understand:

- which external resources luca currently manages on the overview;
- where current tasks, PRDs, research, memory, and open decisions live.

Optimize for scanning, judgment, and resuming work. Avoid marketing copy, decorative visuals, and inflated presentation.

## Visual Direction

Use a Google Material-inspired style:

- clear hierarchy;
- lightweight cards;
- intentional whitespace;
- low-saturation colors;
- content-first composition;
- scannable state.

Do not use large dark surfaces, strong gradients, decorative illustrations, floating light effects, or complex animation.

## Layout

- Max content width: around `1120px`.
- Page margin: `24px-36px` on desktop, `16px-22px` on mobile.
- First viewport of the dashboard: key project-state summary only.
- Dashboard body: summary metrics and project-domain detail. Topic navigation exists only in the shared top tabs.
- Topic page body: one subject with its complete detail.
- Do not nest cards inside cards.
- Use cards for standalone explanatory blocks.
- Use tables for ledgers, resources, services, and status lists.

Page architecture:

1. Shared header: luca name and last updated time.
2. Shared navigation: overview, current work, bugs, product and research, memory and agreements.
3. `dashboard.html`: key counts, status summary, the three most recently created TODOs directly below the work summary, and project-domain resources and services. Recent TODOs are not status-filtered. The external-resource table uses exactly three columns: name, introduction, and operation. Introduction merges the source “function” and “one-line understanding” values into one readable cell without dropping either fact. “Remove” copies a complete model instruction that follows the project removal protocol, but never mutates project state from the page. Do not generate self-introduction or topic-entry cards in the body.
4. `todo.html`: treat a TODO and an Epic as the same top-level work-item concept; an Epic is a special item containing child TODOs. It occupies one row or card, with children collapsed by default. Epic has no numeric TODO ID: its ID cell and kanban label show only `EPIC`, linked directly to the corresponding `projects/todo/epic/<slug>.md` source; never expose the slug as display text and never invent a numeric ID. TODO list tables use exactly four columns: ID, item, status, and operation. Do not keep a separate summary column. Use one fixed track system throughout the list: ID is `82px`, status is `92px`, operation is `116px`, and item consumes the remaining width. Keep the operation track but leave its visible header blank; preserve the column semantics with an accessible name. Normal TODO rows, Epic collapsed summaries, and expanded child tables must reuse the exact same status and operation tracks so the header and every status badge share one left edge. In every normal TODO and expanded Epic-child row, the item cell uses a two-line hierarchy: a larger, heavier title followed by the former summary as smaller muted supporting text. An Epic keeps the first ID cell and uses one `colspan` cell from the item column through status and operation. Its collapsed summary internally aligns those three visual fields; the item field uses the same two-line hierarchy, with the title followed by a low-emphasis `N 个 TODO` total computed from `projects/todo/index.md`, and its compact segmented progress composition as the supporting second line. Show only this total beside the title; do not restore a textual open/completed/abandoned summary. When opened, the child TODO table consumes the full spanned width instead of being constrained to the item column. In every Epic list row, compute the progress composition from child TODO states: in progress, ready, waiting for dependencies, on hold, completed, and abandoned. Segment width is proportional to the child count; dependency waiting is derived only from explicit ledger dependency IDs. Every TODO and Epic item in list and kanban views has two compact copy-only actions: “施工” prepares a feasibility brief under the `skills/todo.md` “实施 TODO” protocol for TODOs or a progress brief under the “推进 Epic” protocol for Epics, and explicitly waits for user approval; “聊聊” prepares a status-discussion instruction containing the real TODO ID or the Epic title and slug. Hide these controls by default and reveal them only when their row/card is hovered or contains keyboard focus; on devices without hover, keep a visible usable fallback. These controls must never mutate a ledger or start implementation directly. Provide a CSS-only list/kanban switch. The kanban columns are in progress, ready, waiting for dependencies, and on hold. Completed and abandoned top-level items appear at the end in collapsed native `details` sections.
5. `todo/TODO_NNNN.html`: provide a room-native detail page for every numbered TODO. The header shows ID, title, ledger status, dates, explicit dependencies, and Epic ownership. YAML front matter belongs only to this metadata header and must never render as body content. Omit the source document's first H1 when it duplicates the page title. Render the remaining Markdown as a deliberate reading surface: use one consistent `24px-28px` content inset for every block, dark explicit H2/H3 hierarchy, readable body color and line height, standard indentation for ordered/unordered/nested/task lists, and coherent spacing for paragraphs, code, blockquotes, rules, and tables. Do not let headings or lists escape the body text baseline. All TODO links on the overview, list, kanban, and Epic children use this detail route. The Markdown file remains the fact source and is linked in the footer.
6. `bugs.html`: open bugs and recently fixed items.
7. `product.html`: PRDs, product proposals, and EXPs.
8. `memory.html`: collaboration agreements, memory entry, and open questions.
9. Each page ends with its own sources.

Do not restore self-introduction, the former assistant / partner / steward cards, the working-style section, a capability tab, or a capability page. Capabilities and self-description belong to luca itself, not the project room. Project-domain content belongs on the dashboard; do not restore a project-domain navigation tab or standalone content page.

## Typography

- Font stack: system sans-serif.
- Body font size: `13px`.
- Body line height: `1.5-1.6`.
- H1: `28px-32px`.
- H2: `16px-18px`.
- H3: `13px-14px`.
- Tags and source notes: `12px`.
- Do not scale font size with viewport width.
- Letter spacing must be `0`.

## Color

Keep color restrained. The page must not be dominated by one hue.

Recommended tokens:

```css
--bg: #f3f5f8;
--panel: #ffffff;
--panel-soft: #f9fafc;
--text: #1b2430;
--muted: #667386;
--quiet: #8a95a6;
--line: #dfe4ec;
--line-strong: #cbd3df;
--accent: #285ea8;
--accent-soft: #e7effb;
--warn: #805a12;
--warn-soft: #fff6dd;
```

Usage rules:

- Use light gray for the page background.
- Use dark gray for primary text, not pure black.
- Use muted color for secondary text.
- Use accent color only for tags, thin emphasis, state hints, and small guidance.
- Use warm pale yellow for empty states; it is not an error state.

## Cards

- Border radius: `8px`.
- Padding: `12px-16px`.
- Border: `1px solid var(--line)`.
- Shadow must be subtle and not look like a modal.
- Card content must be short and scannable.
- A thin left accent bar is allowed.
- Do not use large colored blocks.

## Tables

Use tables for resources, services, TODO, PRD, and EXP.

- Header background: pale gray-blue.
- Cell padding: `8px-12px`.
- Use thin row separators.
- Every table containing two or more body rows uses one shared, subtle full-row hover background. Apply the same feedback when a row contains keyboard focus. Do not add the effect to table headers, empty tables, or one-row information tables.
- Use `code` for long paths, commands, IDs, and filenames.
- Allow horizontal scrolling when content is wide.
- Do not shrink content until it becomes unreadable.

## State Expression

- Prefer short text and lightweight tags.
- Ledger status should reuse the emoji from the relevant index.
- For missing, uninitialized, or empty areas, show an explicit empty state.
- Mark assumptions as assumptions. Do not mix them with facts.

## Responsive Behavior

- Desktop: two-column or three-column grid.
- Narrow screens: single column.
- Tables may scroll horizontally.
- Text must not overflow cards, buttons, or table cells.

## HTML Constraints

- Generate a set of static HTML files with `dashboard.html` as the fixed entry and `todo/TODO_NNNN.html` as the stable numbered TODO detail route.
- Share local CSS through `room.css`.
- No external network resources.
- No framework.
- No JavaScript unless the user explicitly asks for interaction. When interaction is requested, keep it local and minimal. Copy-to-clipboard actions may prepare a model instruction, but must not directly remove resources, edit ledgers, or perform project-state transitions.
- No embedded image, SVG illustration, or icon library.
- The page must open directly from the local filesystem.

## Content Constraints

- All room pages display confirmed facts only.
- Do not read state back from room pages.
- Do not treat room pages as ledgers.
- Do not create new project facts inside room pages.
- If a source file is missing, show the missing area instead of inventing content.

## Update Procedure

When updating the room:

1. Read `skills/room.md`.
2. Read this design specification.
3. Read the current fact sources.
4. Fully regenerate the overview, all topic pages, all numbered TODO detail pages, and shared stylesheet under `projects/room/`.
5. Validate that every navigation target exists and only one navigation item is active per page.
6. Report the entry path, sources read, and missing areas.

Do not patch old HTML by guessing local changes. When visual rules change, this file is the source of truth.
