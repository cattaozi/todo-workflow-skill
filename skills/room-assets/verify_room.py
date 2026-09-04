from __future__ import annotations

from pathlib import Path
import hashlib
import re
import sys

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[2]
BASELINE = ROOT / "skills" / "room-assets"
RUNTIME = ROOT / "projects" / "room"
TODO_INDEX = ROOT / "projects" / "todo" / "index.md"
TODO_LEDGER = ROOT / "projects" / "todo"

TODO_ROW_RE = re.compile(
    r"^\| \[#(?P<id>\d{4})\]\(TODO_(?P=id)\.md\) \| "
    r"(?P<title>.*?) \| (?P<status>[^|]+?) \| (?P<created>[^|]*?) \| "
    r"(?P<completed>[^|]*?) \| (?P<dependencies>[^|]*?) \| (?P<note>.*?) \|$"
)
TODO_HTML_RE = re.compile(r"(?:^|/)TODO_(\d{4})\.html$")
EPIC_HEADING_RE = re.compile(r"^\[(?P<title>.+)\]\(epic/(?P<slug>[^)]+)\.md\)$")
EPIC_LINK_RE = re.compile(r"(?:^|/)epic/(?P<slug>[^/]+)\.md$")

INDEX_STATUS_TO_DETAIL = {
    "⚪": {"todo"},
    "🟡": {"in_progress"},
    "⏸️": {"on_hold"},
    "🟢": {"done", "completed"},
    "⚫": {"abandoned"},
}
TERMINAL_INDEX_STATUS_TO_ROOM = {"🟢": "completed", "⚫": "abandoned"}
NON_TERMINAL_ROOM_STATUSES = {"ready", "waiting", "progress", "hold"}
ROOM_STATUS_LABELS = {
    "ready": "待办",
    "waiting": "等待依赖",
    "progress": "进行中",
    "hold": "搁置",
    "completed": "已完成",
    "abandoned": "已废弃",
}
EXPECTED_SITE_IDENTITY = "luca · 账本"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(page: Path, selectors: tuple[str, ...]) -> list[str]:
    if not page.exists():
        return [f"缺少页面：{page.relative_to(ROOT)}"]
    soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
    errors: list[str] = []
    for selector in selectors:
        if soup.select_one(selector) is None:
            errors.append(f"{page.relative_to(ROOT)} 缺少结构：{selector}")
    return errors


def require_site_identity(page: Path) -> list[str]:
    if not page.exists():
        return []
    soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
    identity = soup.select_one("main.page > header.site-head strong")
    actual = identity.get_text(" ", strip=True) if identity is not None else ""
    if actual != EXPECTED_SITE_IDENTITY:
        return [
            f"{page.relative_to(ROOT)} 页头身份应为"
            f"“{EXPECTED_SITE_IDENTITY}”，实际为“{actual}”"
        ]
    return []


def parse_todo_index() -> tuple[dict[str, dict[str, object]], dict[str, list[str]], list[str]]:
    records: dict[str, dict[str, object]] = {}
    epics: dict[str, list[str]] = {}
    errors: list[str] = []
    if not TODO_INDEX.exists():
        return records, epics, ["缺少 TODO 事实源：projects/todo/index.md"]

    section = ""
    for lineno, line in enumerate(TODO_INDEX.read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("## "):
            section = line[3:].strip()
            if EPIC_HEADING_RE.fullmatch(section):
                epics.setdefault(section, [])
            continue

        match = TODO_ROW_RE.fullmatch(line)
        if match is None:
            continue

        todo_id = match.group("id")
        if todo_id in records:
            errors.append(f"projects/todo/index.md 重复 TODO：#{todo_id}")
            continue

        status = match.group("status").strip()
        if status not in INDEX_STATUS_TO_DETAIL:
            errors.append(
                f"projects/todo/index.md:{lineno} 的 #{todo_id} 使用非规范状态：{status}"
            )

        dependencies = re.findall(r"#(\d{4})", match.group("dependencies"))
        records[todo_id] = {
            "title": match.group("title").strip(),
            "status": status,
            "created": match.group("created").strip(),
            "completed": match.group("completed").strip(),
            "dependencies": dependencies,
            "section": section,
            "line": lineno,
        }

        if section == "待办" and status in TERMINAL_INDEX_STATUS_TO_ROOM:
            errors.append(f"projects/todo/index.md 的已结束散户 TODO #{todo_id} 仍位于待办区")
        elif section == "归档" and status not in TERMINAL_INDEX_STATUS_TO_ROOM:
            errors.append(f"projects/todo/index.md 的未结束散户 TODO #{todo_id} 错放在归档区")
        elif EPIC_HEADING_RE.fullmatch(section):
            epics[section].append(todo_id)

    ledger_ids = {
        path.stem.removeprefix("TODO_")
        for path in TODO_LEDGER.glob("TODO_[0-9][0-9][0-9][0-9].md")
    }
    missing_from_index = sorted(ledger_ids - records.keys())
    missing_details = sorted(records.keys() - ledger_ids)
    if missing_from_index:
        errors.append("TODO 详情未进入 index：" + ", ".join(f"#{item}" for item in missing_from_index))
    if missing_details:
        errors.append("TODO index 缺少详情文件：" + ", ".join(f"#{item}" for item in missing_details))

    for todo_id, record in records.items():
        detail = TODO_LEDGER / f"TODO_{todo_id}.md"
        if not detail.exists():
            continue
        status_match = re.search(
            r"^status:\s*(\S+)\s*$", detail.read_text(encoding="utf-8"), re.MULTILINE
        )
        if status_match is None:
            errors.append(f"projects/todo/TODO_{todo_id}.md 缺少 frontmatter status")
            continue
        allowed = INDEX_STATUS_TO_DETAIL.get(str(record["status"]), set())
        if status_match.group(1) not in allowed:
            errors.append(
                f"TODO #{todo_id} 的 index 状态 {record['status']} "
                f"与详情状态 {status_match.group(1)} 不一致"
            )

    return records, epics, errors


def todo_id_from_row(row: object) -> str | None:
    for anchor in row.find_all("a", href=True):
        match = TODO_HTML_RE.search(anchor.get("href", ""))
        if match:
            return match.group(1)
    return None


def item_identity(node: object) -> tuple[str, str] | None:
    """Return the stable ledger identity carried by a list row or board card."""
    for anchor in node.find_all("a", href=True):
        href = anchor.get("href", "")
        todo_match = TODO_HTML_RE.search(href)
        if todo_match:
            return "todo", todo_match.group(1)
        epic_match = EPIC_LINK_RE.search(href)
        if epic_match:
            return "epic", epic_match.group("slug")
    return None


def validate_room_data(
    dashboard_soup: BeautifulSoup,
    todo_soup: BeautifulSoup,
    records: dict[str, dict[str, object]],
    epics: dict[str, list[str]],
) -> list[str]:
    errors: list[str] = []
    expected_epics: dict[str, list[str]] = {}
    for heading, members in epics.items():
        match = EPIC_HEADING_RE.fullmatch(heading)
        if match is not None:
            expected_epics[match.group("slug")] = members

    room_rows: dict[str, object] = {}
    for row in todo_soup.select("tr.work-row"):
        todo_id = todo_id_from_row(row)
        if todo_id is None:
            errors.append("projects/room/todo.html 存在无法识别 TODO 编号的数据行")
            continue
        if todo_id in room_rows:
            errors.append(f"projects/room/todo.html 重复 TODO：#{todo_id}")
            continue
        room_rows[todo_id] = row

    missing_rows = sorted(records.keys() - room_rows.keys())
    extra_rows = sorted(room_rows.keys() - records.keys())
    if missing_rows:
        errors.append("Room 事项列表缺少：" + ", ".join(f"#{item}" for item in missing_rows))
    if extra_rows:
        errors.append("Room 事项列表存在账本外对象：" + ", ".join(f"#{item}" for item in extra_rows))

    for todo_id in sorted(records.keys() & room_rows.keys()):
        record = records[todo_id]
        row = room_rows[todo_id]
        room_status = row.get("data-status", "")
        badge = row.select_one(".status")
        badge_text = badge.get_text(" ", strip=True) if badge is not None else ""
        expected_badge = ROOM_STATUS_LABELS.get(room_status)
        if expected_badge is None:
            errors.append(f"Room TODO #{todo_id} 使用未知 data-status：{room_status}")
        elif badge_text != expected_badge:
            errors.append(
                f"Room TODO #{todo_id} 的 data-status={room_status} "
                f"与状态徽标“{badge_text}”不一致"
            )

        terminal_status = TERMINAL_INDEX_STATUS_TO_ROOM.get(str(record["status"]))
        if terminal_status is not None and room_status != terminal_status:
            errors.append(
                f"已结束 TODO #{todo_id} 未同步到 Room："
                f"账本={terminal_status}，Room={room_status}"
            )
        elif terminal_status is None and room_status not in NON_TERMINAL_ROOM_STATUSES:
            errors.append(f"未结束 TODO #{todo_id} 在 Room 中被标记为 {room_status}")

    actual_epics: dict[str, object] = {}
    for row in todo_soup.select("tr.epic-row"):
        identity = item_identity(row)
        if identity is None or identity[0] != "epic":
            errors.append("projects/room/todo.html 存在无法识别的 EPIC 顶层行")
            continue
        slug = identity[1]
        if slug in actual_epics:
            errors.append(f"projects/room/todo.html 重复 EPIC：{slug}")
            continue
        actual_epics[slug] = row

        epic_status = row.get("data-status", "")
        badge = row.select_one(":scope > td[colspan] > details > summary > .status")
        badge_text = badge.get_text(" ", strip=True) if badge is not None else ""
        expected_badge = ROOM_STATUS_LABELS.get(epic_status)
        if expected_badge is None:
            errors.append(f"Room EPIC {slug} 使用未知 data-status：{epic_status}")
        elif badge_text != expected_badge:
            errors.append(
                f"Room EPIC {slug} 的 data-status={epic_status} "
                f"与状态徽标“{badge_text}”不一致"
            )

        table = row.parent.parent if row.parent is not None else None
        wrap = table.parent if table is not None else None
        container = wrap.parent if wrap is not None else None
        is_top_level = (
            getattr(row.parent, "name", None) == "tbody"
            and getattr(table, "name", None) == "table"
            and getattr(wrap, "name", None) == "div"
            and "table-wrap" in wrap.get("class", [])
            and (
                container.get("id") == "list-view"
                or (
                    getattr(container, "name", None) == "details"
                    and "closed-section" in container.get("class", [])
                )
            )
        )
        if not is_top_level:
            errors.append(f"Room EPIC {slug} 未作为顶层事项展示")

        child_rows = row.select(
            ":scope > td[colspan] > details > .epic-children "
            "> table.work-table > tbody > tr.work-row"
        )
        actual_members = [todo_id_from_row(child) for child in child_rows]
        if None in actual_members:
            errors.append(f"Room EPIC {slug} 存在无法识别的子 TODO")
        expected_members = expected_epics.get(slug)
        if expected_members is not None and actual_members != expected_members:
            errors.append(
                f"Room EPIC {slug} 子项归属或顺序与账本不一致："
                f"Room={actual_members}，账本={expected_members}"
            )

    missing_epics = sorted(expected_epics.keys() - actual_epics.keys())
    extra_epics = sorted(actual_epics.keys() - expected_epics.keys())
    if missing_epics:
        errors.append("Room 事项列表缺少 EPIC：" + ", ".join(missing_epics))
    if extra_epics:
        errors.append("Room 事项列表存在账本外 EPIC：" + ", ".join(extra_epics))

    open_rows = todo_soup.select(
        "#list-view > .table-wrap > table.work-table > tbody > tr"
    )
    open_items: dict[tuple[str, str], str] = {}
    for row in open_rows:
        identity = item_identity(row)
        if identity is None:
            errors.append("todo.html 开放列表存在无法识别的顶层事项")
            continue
        if identity in open_items:
            errors.append(f"todo.html 开放列表重复事项：{identity}")
        open_items[identity] = row.get("data-status", "")

    board_items: dict[tuple[str, str], str] = {}
    for card in todo_soup.select("#board-view article.board-card"):
        identity = item_identity(card)
        if identity is None:
            errors.append("todo.html 看板存在无法识别的事项卡片")
            continue
        if identity in board_items:
            errors.append(f"todo.html 看板重复事项：{identity}")
        board_items[identity] = card.get("data-status", "")

    if open_items != board_items:
        errors.append(
            "todo.html 列表与看板的开放事项或状态不一致："
            f"列表={open_items}，看板={board_items}"
        )

    for column in todo_soup.select("#board-view .board-col"):
        counter = column.select_one(":scope > h2 > span")
        counter_text = counter.get_text(strip=True) if counter is not None else ""
        cards = column.select(":scope > article.board-card")
        if not counter_text.isdigit() or int(counter_text) != len(cards):
            heading = column.select_one(":scope > h2")
            heading_text = heading.get_text(" ", strip=True) if heading is not None else "?"
            errors.append(
                f"todo.html 看板列“{heading_text}”计数错误："
                f"摘要={counter_text}，实际={len(cards)}"
            )
        heading_label = "".join(
            str(child) for child in column.select_one(":scope > h2").find_all(string=True, recursive=False)
        ).strip()
        expected_column_status = {
            "进行中": "progress",
            "待办": "ready",
            "等待依赖": "waiting",
            "搁置": "hold",
        }.get(heading_label)
        if expected_column_status is None:
            errors.append(f"todo.html 看板存在未知列：{heading_label or '?'}")
        else:
            misplaced = [
                item_identity(card)
                for card in cards
                if card.get("data-status") != expected_column_status
            ]
            if misplaced:
                errors.append(
                    f"todo.html 看板列“{heading_label}”混入其他状态事项："
                    f"{misplaced}"
                )

    detail_ids = {
        path.stem.removeprefix("TODO_")
        for path in (RUNTIME / "todo").glob("TODO_[0-9][0-9][0-9][0-9].html")
    }
    missing_detail_pages = sorted(records.keys() - detail_ids)
    extra_detail_pages = sorted(detail_ids - records.keys())
    if missing_detail_pages:
        errors.append("Room 缺少 TODO 详情页：" + ", ".join(f"#{item}" for item in missing_detail_pages))
    if extra_detail_pages:
        errors.append("Room 存在账本外 TODO 详情页：" + ", ".join(f"#{item}" for item in extra_detail_pages))

    for todo_id in sorted(records.keys() & detail_ids):
        record = records[todo_id]
        page = RUNTIME / "todo" / f"TODO_{todo_id}.html"
        detail_soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
        badge = detail_soup.select_one(".detail-head .status")
        badge_text = badge.get_text(" ", strip=True) if badge is not None else ""
        terminal_status = TERMINAL_INDEX_STATUS_TO_ROOM.get(str(record["status"]))
        if terminal_status is not None:
            expected_badge = ROOM_STATUS_LABELS[terminal_status]
            if badge_text != expected_badge:
                errors.append(
                    f"Room TODO #{todo_id} 详情页终态未同步："
                    f"应为“{expected_badge}”，实际为“{badge_text}”"
                )
        elif badge_text in {"已完成", "已废弃"}:
            errors.append(f"未结束 TODO #{todo_id} 的 Room 详情页显示为“{badge_text}”")

    metric = dashboard_soup.select_one(".metric-grid > .metric[href='todo.html']")
    if metric is None or metric.select_one("strong") is None:
        errors.append("projects/room/dashboard.html 缺少开放事项指标")
    else:
        value = metric.select_one("strong").get_text(strip=True)
        if not value.isdigit() or int(value) != len(open_rows):
            errors.append(
                "dashboard 开放事项指标与 todo.html 不一致："
                f"dashboard={value}，事项页={len(open_rows)}"
            )
        summary = metric.select_one("small")
        summary_match = re.fullmatch(
            r"(\d+) 条 TODO · (\d+) 个 EPIC",
            summary.get_text(" ", strip=True) if summary is not None else "",
        )
        if summary_match is None:
            errors.append("dashboard 开放事项摘要缺少 TODO / EPIC 结构化计数")
        else:
            todo_count, epic_count = map(int, summary_match.groups())
            if todo_count != len(records):
                errors.append(
                    f"dashboard TODO 总数错误：dashboard={todo_count}，账本={len(records)}"
                )
            if epic_count != len(epics):
                errors.append(
                    f"dashboard EPIC 总数错误：dashboard={epic_count}，账本={len(epics)}"
                )

    for status in ("completed", "abandoned"):
        section = todo_soup.select_one(
            f"main.page > details.closed-section[data-status-group='{status}']"
        )
        if section is None:
            continue
        rows = section.select(":scope > .table-wrap > table.work-table > tbody > tr")
        misplaced = [
            item_identity(row)
            for row in rows
            if row.get("data-status") != status
        ]
        if misplaced:
            errors.append(
                f"todo.html 的 {status} 顶层分区混入其他状态事项："
                f"{misplaced}"
            )
        counter = section.select_one(":scope > summary > span")
        counter_text = counter.get_text(strip=True) if counter is not None else ""
        if not counter_text.isdigit() or int(counter_text) != len(rows):
            errors.append(
                f"todo.html 的 {status} 顶层计数错误："
                f"摘要={counter_text}，实际={len(rows)}"
            )

    return errors


def main() -> int:
    errors: list[str] = []
    records, epics, ledger_errors = parse_todo_index()
    errors.extend(ledger_errors)
    for name in ("room.css", "room.js"):
        baseline = BASELINE / name
        runtime = RUNTIME / name
        if not baseline.exists() or not runtime.exists():
            errors.append(f"缺少 UI 资产：{name}")
        elif digest(baseline) != digest(runtime):
            errors.append(f"运行时 {name} 偏离版本化基线")

    shared = ("main.page", "nav.nav", 'link[rel="stylesheet"]')
    for name in ("dashboard.html", "todo.html", "bugs.html", "product.html", "memory.html"):
        page = RUNTIME / name
        errors.extend(require(page, shared))
        errors.extend(require_site_identity(page))

    dashboard_page = RUNTIME / "dashboard.html"
    errors.extend(require(dashboard_page, (".latest-grid", ".latest-card")))
    dashboard_soup = None
    if dashboard_page.exists():
        dashboard_soup = BeautifulSoup(
            dashboard_page.read_text(encoding="utf-8"), "html.parser"
        )
        latest_cards = dashboard_soup.select(".latest-grid > .latest-card")
        if len(latest_cards) != 3:
            errors.append(
                "projects/room/dashboard.html 的最新 TODO 必须保持三张卡片"
            )

    errors.extend(
        require(
            RUNTIME / "todo.html",
            (
                ".view-switch",
                ".filters",
                "#work-search",
                "#list-view",
                "#board-view",
                "table.work-table",
                "col.id-col",
                "col.state-col",
                "col.action-col",
            ),
        )
    )

    todo_page = RUNTIME / "todo.html"
    todo_soup = None
    if todo_page.exists():
        todo_soup = BeautifulSoup(todo_page.read_text(encoding="utf-8"), "html.parser")
        if todo_soup.select_one("main.page > .metric-grid") is not None:
            errors.append("projects/room/todo.html 不应展示汇总指标卡")
        epic_mains = todo_soup.select("#list-view .epic-main")
        inline_totals = todo_soup.select("#list-view .epic-main > .work-title + small")
        if len(inline_totals) != len(epic_mains):
            errors.append("projects/room/todo.html 的 EPIC 总数必须紧邻标题")
        segment_bars = todo_soup.select("#list-view .epic-main > .segments")
        if len(segment_bars) != len(epic_mains) or any(
            not bar.select(":scope > .seg") for bar in segment_bars
        ):
            errors.append("projects/room/todo.html 的 EPIC 必须提供结构化进度分段")
        open_rows = todo_soup.select(
            "#list-view > .table-wrap > table.work-table > tbody > tr"
        )
        leaked_closed = [
            row.get("data-status", "")
            for row in open_rows
            if row.get("data-status") in {"completed", "abandoned"}
        ]
        if leaked_closed:
            errors.append("projects/room/todo.html 的开放列表混入已完成或已废弃事项")
        nested_closed = todo_soup.select_one(
            "main.page > section.section details.closed-section, "
            "#list-view > details.closed-section, "
            "#board-view > details.closed-section"
        )
        if nested_closed is not None:
            errors.append("projects/room/todo.html 的归档折叠区必须脱离当前事项容器")
        for status in ("completed", "abandoned"):
            selector = (
                "main.page > details.closed-section"
                f"[data-status-group='{status}']"
            )
            section = todo_soup.select_one(selector)
            if section is None:
                errors.append(f"projects/room/todo.html 缺少 {status} 折叠区")
            elif section.has_attr("open"):
                errors.append(f"projects/room/todo.html 的 {status} 折叠区不应默认展开")

    if dashboard_soup is not None and todo_soup is not None and records:
        errors.extend(validate_room_data(dashboard_soup, todo_soup, records, epics))

    detail_pages = sorted((RUNTIME / "todo").glob("TODO_[0-9][0-9][0-9][0-9].html"))
    if not detail_pages:
        errors.append("缺少 TODO 详情页")
    else:
        for page in detail_pages:
            errors.extend(require(
                page,
                ("main.page", ".detail-head", "article.section.markdown-body"),
            ))
            errors.extend(require_site_identity(page))

    if errors:
        print("Room UI 门禁失败：", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Room UI 门禁通过：CSS / JS 与版本化基线一致，"
        f"5 个主页面、{len(detail_pages)} 个 TODO 详情页结构有效；"
        "TODO 账本、Room 事项与 dashboard 指标一致。"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
