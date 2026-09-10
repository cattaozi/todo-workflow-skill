from __future__ import annotations

from collections import Counter
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
PROJECTS_README = ROOT / "projects" / "README.md"

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
EPIC_STATUS_PRECEDENCE = (
    "progress",
    "waiting",
    "ready",
    "hold",
    "completed",
    "abandoned",
)
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


def parse_project_domain() -> tuple[list[list[str]], list[list[str]], list[str]]:
    resources: list[list[str]] = []
    services: list[list[str]] = []
    errors: list[str] = []
    if not PROJECTS_README.exists():
        return resources, services, ["缺少项目域事实源：projects/README.md"]

    section = ""
    for lineno, line in enumerate(PROJECTS_README.read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        if section not in {"外部资源", "服务定义"} or not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells or cells[0] in {"名称", "服务"} or set(cells[0]) == {"-"}:
            continue
        expected_width = 5 if section == "外部资源" else 8
        if len(cells) != expected_width:
            errors.append(
                f"projects/README.md:{lineno} 的{section}表格列数应为 "
                f"{expected_width}，实际为 {len(cells)}"
            )
            continue
        (resources if section == "外部资源" else services).append(cells)

    return resources, services, errors


def validate_project_domain(
    dashboard_soup: BeautifulSoup,
    resources: list[list[str]],
    services: list[list[str]],
) -> list[str]:
    errors: list[str] = []
    section = dashboard_soup.select_one("#project-domain")
    if section is None:
        return ["projects/room/dashboard.html 缺少项目域区域"]

    resource_table = section.select_one(":scope > .table-wrap > table")
    service_section = dashboard_soup.select_one("#project-domain + section.section")
    service_table = (
        service_section.select_one(":scope > .table-wrap > table")
        if service_section is not None
        else None
    )
    if resource_table is None or service_table is None:
        return ["projects/room/dashboard.html 应保持独立的资源表和服务表"]

    resource_rows = resource_table.select("tbody > tr")
    actual_resource_names = [
        row.select_one(":scope > td").get_text(" ", strip=True)
        for row in resource_rows
    ]
    expected_resource_names = [row[0] for row in resources]
    if actual_resource_names != expected_resource_names:
        errors.append(
            "dashboard 外部资源与 projects/README.md 不一致："
            f"dashboard={actual_resource_names}，README={expected_resource_names}"
        )

    for dashboard_row, source_row in zip(resource_rows, resources):
        cells = dashboard_row.select(":scope > td")
        actual_summary = cells[1].get_text(" ", strip=True) if len(cells) > 1 else ""
        expected_summary = f"{source_row[3]} {source_row[4]}".strip()
        if actual_summary != expected_summary:
            errors.append(f"dashboard 外部资源 {source_row[0]} 的简介与 README 不一致")

    counter = section.select_one(":scope > .section-head > span")
    counter_text = counter.get_text(" ", strip=True) if counter is not None else ""
    if counter_text != f"{len(resources)} 项":
        errors.append(
            f"dashboard 外部资源计数错误："
            f"dashboard={counter_text}，README={len(resources)} 项"
        )

    service_rows = service_table.select("tbody > tr")
    actual_service_names = [
        row.select_one(":scope > td").get_text(" ", strip=True)
        for row in service_rows
    ]
    expected_service_names = [row[0] for row in services]
    if actual_service_names != expected_service_names:
        errors.append(
            "dashboard 服务清单与 projects/README.md 不一致："
            f"dashboard={actual_service_names}，README={expected_service_names}"
        )

    service_counter = service_section.select_one(":scope > .section-head > span")
    service_counter_text = (
        service_counter.get_text(" ", strip=True) if service_counter is not None else ""
    )
    if service_counter_text != f"{len(services)} 项":
        errors.append(
            f"dashboard 服务计数错误："
            f"dashboard={service_counter_text}，README={len(services)} 项"
        )

    for dashboard_row, source_row in zip(service_rows, services):
        cells = [cell.get_text(" ", strip=True) for cell in dashboard_row.select(":scope > td")]
        expected = [source_row[0], source_row[2], source_row[3], source_row[5].strip("`")]
        if cells != expected:
            errors.append(f"dashboard 服务 {source_row[0]} 的展示数据与 README 不一致")

    return errors


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


def displayed_todo_count(node: object) -> int | None:
    """Read the EPIC member count shown beside its title."""
    summary = node.select_one(".work-title + small")
    if summary is None:
        return None
    match = re.fullmatch(r"(\d+) 个 TODO", summary.get_text(" ", strip=True))
    return int(match.group(1)) if match is not None else None


def segment_status_counts(epic_row: object) -> tuple[Counter[str], list[str]]:
    """Read the status totals encoded by an EPIC's segmented bar."""
    counts: Counter[str] = Counter()
    errors: list[str] = []
    for segment in epic_row.select(
        ":scope > td[colspan] > details > summary .segments > .seg"
    ):
        statuses = [
            name.removeprefix("seg-")
            for name in segment.get("class", [])
            if name.startswith("seg-")
        ]
        flex = re.search(r"(?:^|;)\s*flex:\s*(\d+)\s*(?:;|$)", segment.get("style", ""))
        if len(statuses) != 1 or flex is None:
            errors.append("存在无法识别状态或数量的色条分段")
            continue
        counts[statuses[0]] += int(flex.group(1))
    return counts, errors


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

        shown_count = displayed_todo_count(row)
        if shown_count != len(child_rows):
            errors.append(
                f"Room EPIC {slug} 的 TODO 总数错误："
                f"摘要={shown_count}，实际子项={len(child_rows)}"
            )

        child_status_counts = Counter(child.get("data-status", "") for child in child_rows)
        segment_counts, segment_errors = segment_status_counts(row)
        for message in segment_errors:
            errors.append(f"Room EPIC {slug} {message}")
        if segment_counts != child_status_counts:
            errors.append(
                f"Room EPIC {slug} 的色条聚合错误："
                f"色条={dict(segment_counts)}，实际子项={dict(child_status_counts)}"
            )

        expected_epic_status = next(
            (status for status in EPIC_STATUS_PRECEDENCE if child_status_counts[status]),
            None,
        )
        if epic_status != expected_epic_status:
            errors.append(
                f"Room EPIC {slug} 的顶层状态错误："
                f"顶层={epic_status}，按子项应为={expected_epic_status}"
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
        if row.get("data-status") == "hold":
            errors.append(f"todo.html 当前事项主容器混入搁置事项：{identity}")

    board_items: dict[tuple[str, str], str] = {}
    for card in todo_soup.select("#board-view article.board-card"):
        identity = item_identity(card)
        if identity is None:
            errors.append("todo.html 看板存在无法识别的事项卡片")
            continue
        if identity in board_items:
            errors.append(f"todo.html 看板重复事项：{identity}")
        board_items[identity] = card.get("data-status", "")
        if identity[0] == "epic":
            expected_count = len(expected_epics.get(identity[1], []))
            shown_count = displayed_todo_count(card)
            if shown_count != expected_count:
                errors.append(
                    f"todo.html 看板 EPIC {identity[1]} 的 TODO 总数错误："
                    f"摘要={shown_count}，账本={expected_count}"
                )

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

    hold_rows = todo_soup.select(
        "main.page > details.closed-section[data-status-group='hold'] "
        "> .table-wrap > table.work-table > tbody > tr"
    )
    metric = dashboard_soup.select_one(".metric-grid > .metric[href='todo.html']")
    if metric is None or metric.select_one("strong") is None:
        errors.append("projects/room/dashboard.html 缺少开放事项指标")
    else:
        value = metric.select_one("strong").get_text(strip=True)
        expected_open_count = len(open_rows) + len(hold_rows)
        if not value.isdigit() or int(value) != expected_open_count:
            errors.append(
                "dashboard 开放事项指标与 todo.html 不一致："
                f"dashboard={value}，事项页={expected_open_count}"
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

    for status in ("hold", "completed", "abandoned"):
        section = todo_soup.select_one(
            f"main.page > details.closed-section[data-status-group='{status}']"
        )
        if section is None:
            errors.append(f"todo.html 缺少 {status} 独立顶层分区")
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
    resources, services, project_errors = parse_project_domain()
    errors.extend(project_errors)
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
        errors.extend(validate_project_domain(dashboard_soup, resources, services))

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
        "TODO 账本、Room 事项、项目域与 dashboard 数据一致。"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
