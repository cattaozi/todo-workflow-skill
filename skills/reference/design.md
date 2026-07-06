# Design — luca room dashboard specification

> This file defines the visual and interaction rules for `projects/room/dashboard.html`. It supports `skills/room.md` and keeps dashboard output consistent across luca instances.

## Purpose

The dashboard is an operational workbench, not a landing page.

It must help the user quickly understand:

- who luca is;
- how luca works;
- what luca can do;
- which external resources luca currently manages;
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
- First viewport: identity header plus key state summary.
- Main body: sectioned by topic.
- Do not nest cards inside cards.
- Use cards for standalone explanatory blocks.
- Use tables for ledgers, resources, services, and status lists.

Recommended section order:

1. Header: luca name, role, last updated time.
2. Identity: assistant / partner / steward.
3. Working style: semantic-first, object-first, read-enough-then-stop, close with records.
4. Capability set: capability, playbook, boundary.
5. Project domain: external resources, service definitions, startup entry points.
6. Current work: TODO, Epic groups, archive summary.
7. Product and research: PRD, product proposal, EXP.
8. Memory and agreements: collaboration agreements, long-term memory entry, open questions.
9. Sources: files read, missing areas.

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

Use tables for resources, services, capabilities, TODO, PRD, and EXP.

- Header background: pale gray-blue.
- Cell padding: `8px-12px`.
- Use thin row separators.
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

- Generate one static HTML file.
- Inline CSS.
- No external network resources.
- No framework.
- No JavaScript unless the user explicitly asks for interaction.
- No embedded image, SVG illustration, or icon library.
- The page must open directly from the local filesystem.

## Content Constraints

- The dashboard displays confirmed facts only.
- Do not read state back from the dashboard.
- Do not treat the dashboard as a ledger.
- Do not create new project facts inside the dashboard.
- If a source file is missing, show the missing area instead of inventing content.

## Update Procedure

When updating the dashboard:

1. Read `skills/room.md`.
2. Read this design specification.
3. Read the current fact sources.
4. Fully regenerate `projects/room/dashboard.html`.
5. Report the output path, sources read, and missing areas.

Do not patch old HTML by guessing local changes. When visual rules change, this file is the source of truth.
