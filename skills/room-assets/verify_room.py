from __future__ import annotations

from pathlib import Path
import hashlib
import sys

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[2]
BASELINE = ROOT / "skills" / "room-assets"
RUNTIME = ROOT / "projects" / "room"


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


def main() -> int:
    errors: list[str] = []
    for name in ("room.css", "room.js"):
        baseline = BASELINE / name
        runtime = RUNTIME / name
        if not baseline.exists() or not runtime.exists():
            errors.append(f"缺少 UI 资产：{name}")
        elif digest(baseline) != digest(runtime):
            errors.append(f"运行时 {name} 偏离版本化基线")

    shared = ("main.page", "nav.nav", 'link[rel="stylesheet"]')
    for name in ("dashboard.html", "todo.html", "bugs.html", "product.html", "memory.html"):
        errors.extend(require(RUNTIME / name, shared))

    dashboard_page = RUNTIME / "dashboard.html"
    errors.extend(require(dashboard_page, (".latest-grid", ".latest-card")))
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

    detail_pages = sorted((RUNTIME / "todo").glob("TODO_[0-9][0-9][0-9][0-9].html"))
    if not detail_pages:
        errors.append("缺少 TODO 详情页")
    else:
        for page in detail_pages:
            errors.extend(require(
                page,
                ("main.page", ".detail-head", "article.section.markdown-body"),
            ))

    if errors:
        print("Room UI 门禁失败：", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Room UI 门禁通过：CSS / JS 与版本化基线一致，"
        f"5 个主页面、{len(detail_pages)} 个 TODO 详情页结构有效。"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
