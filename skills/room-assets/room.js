const normalize = (value) =>
  String(value || "")
    .normalize("NFKC")
    .toLocaleLowerCase()
    .replace(/\s+/g, " ")
    .trim();

const matches = (value, tokens) => {
  const corpus = normalize(value);
  return tokens.every((token) => corpus.includes(token));
};

const epicStatusMeta = new Map([
  ["progress", "进行中"],
  ["ready", "可推进"],
  ["waiting", "等待依赖"],
  ["hold", "搁置"],
  ["completed", "已完成"],
  ["abandoned", "已废弃"],
]);

const renderEpicLegends = () => {
  document.querySelectorAll(".epic-main > .segments").forEach((bar) => {
    const existing = bar.nextElementSibling;
    if (existing?.classList.contains("segment-legend")) existing.remove();

    const legend = document.createElement("div");
    legend.className = "segment-legend";
    bar.querySelectorAll(":scope > .seg").forEach((segment) => {
      const statusClass = [...segment.classList]
        .find((className) => className.startsWith("seg-"));
      const status = statusClass?.slice(4) || "";
      const label = epicStatusMeta.get(status);
      const count = Number(segment.style.flexGrow || 0);
      if (!label || !Number.isFinite(count) || count <= 0) return;

      const item = document.createElement("span");
      item.className = "segment-legend-item";
      const dot = document.createElement("i");
      dot.className = `segment-legend-dot seg-${status}`;
      const text = document.createElement("span");
      text.textContent = label;
      const value = document.createElement("b");
      value.textContent = String(count);
      item.append(dot, text, value);
      legend.appendChild(item);
    });
    bar.insertAdjacentElement("afterend", legend);
  });
};

renderEpicLegends();

const removePrompt = (resource) =>
  `请将外部资源「${resource}」移出当前 luca 项目域管理。请按 skills/project.md 的“移出外部资源”协议执行：只删除 projects/links/${resource} 软链，不删除真实项目目录；同步移除 projects/README.md 中该资源及对应服务、projects/scripts/dev-services.sh 中对应服务入口，以及仅属于该资源的待确认事项；不要修改历史 TODO、Epic、PRD、EXP、memory 或 inbox。完成后只按现有页面结构同步 projects/room/dashboard.html 中受影响的项目域数据，不要重新生成整个 projects/room/，不要改动 Room 的 CSS、JS、导航、工具栏、类名或页面骨架；同步前后运行 Room 门禁，并汇报真实目录未被改动。`;

const todoPrompt = {
  start: (id) =>
    `请分析 TODO #${id} 的可实施性，并按 skills/todo.md 的“实施 TODO”协议先生成开工简报给我。请读取该 TODO 的详情、总台账和 Epic 归属（如有），核对当前状态、目标与验收、依赖与阻塞、真实实施入口、影响范围、建议实施路径、验证方案、风险和需要我拍板的事项。此阶段不要修改任何代码、文件、账本或状态；输出开工简报后停下，等我决定如何处理。`,
  discuss: (id) => `我们来聊聊这个 TODO #${id}，你先评估一下它的状态。`,
};

const epicPrompt = {
  start: (title, slug) =>
    `请分析 EPIC「${title}」（${slug}）的可推进性，并按 skills/todo.md 的“推进 Epic”协议先生成推进简报给我。请读取该 Epic 说明文件、TODO 总台账和全部成员，核对当前状态构成、目标与范围、依赖顺序、已就绪成员、阻塞与复活条件、建议推进顺序、验证方式、风险和需要我拍板的事项。此阶段不要修改任何代码、文件、账本或状态；输出推进简报后停下，等我决定如何处理。`,
  discuss: (title, slug) =>
    `我们来聊聊这个 EPIC「${title}」（${slug}），你先评估一下它的状态。`,
};

async function copyText(text) {
  if (navigator.clipboard && window.isSecureContext) {
    await navigator.clipboard.writeText(text);
    return;
  }

  const area = document.createElement("textarea");
  area.value = text;
  area.setAttribute("readonly", "");
  area.style.position = "fixed";
  area.style.opacity = "0";
  document.body.appendChild(area);
  area.select();
  const copied = document.execCommand("copy");
  area.remove();
  if (!copied) throw new Error("copy failed");
}

function promptFor(button) {
  if (button.classList.contains("resource-remove")) {
    const resource = button.dataset.resource || "";
    return resource ? removePrompt(resource) : "";
  }

  const kind = button.dataset.kind || "";
  const id = button.dataset.id || "";
  if (kind === "todo-start" || kind === "todo-discuss") {
    if (!/^\d{4}$/.test(id)) return "";
    return kind === "todo-start" ? todoPrompt.start(id) : todoPrompt.discuss(id);
  }

  if (kind === "epic-start" || kind === "epic-discuss") {
    const slug = button.dataset.slug || "";
    if (!id.trim() || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug)) return "";
    return kind === "epic-start" ? epicPrompt.start(id, slug) : epicPrompt.discuss(id, slug);
  }

  return "";
}

document.addEventListener("click", async (event) => {
  const button = event.target.closest(".copy-action");
  if (!button) return;

  event.preventDefault();
  event.stopPropagation();
  const prompt = promptFor(button);
  if (!prompt) return;

  const original = button.textContent;
  button.disabled = true;
  try {
    await copyText(prompt);
    button.textContent = "已复制";
    button.classList.add("copied");
  } catch {
    button.textContent = "复制失败";
    button.classList.add("copy-failed");
  }

  window.setTimeout(() => {
    button.textContent = original;
    button.classList.remove("copied", "copy-failed");
    button.disabled = false;
  }, 1500);
});

const listView = document.querySelector("#list-view");
const boardView = document.querySelector("#board-view");
const viewButtons = [...document.querySelectorAll("[data-view]")];

viewButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const showList = button.dataset.view === "list";
    viewButtons.forEach((candidate) => {
      candidate.classList.toggle("active", candidate === button);
      candidate.setAttribute("aria-pressed", String(candidate === button));
    });
    if (listView) listView.hidden = !showList;
    if (boardView) boardView.hidden = showList;
  });
});

const searchInput = document.querySelector("#work-search");
const filterButtons = [...document.querySelectorAll(".filter[data-filter]")];

if (searchInput && filterButtons.length && listView && boardView) {
  const activeStatuses = new Set();
  const topRows = [
    ...listView.querySelectorAll(
      ":scope > .table-wrap > table.work-table > tbody > tr",
    ),
    ...document.querySelectorAll(
      "main.page > details.closed-section > .table-wrap > table.work-table > tbody > tr",
    ),
  ];
  const epicDetails = topRows
    .map((row) => row.querySelector(":scope > td[colspan] > details"))
    .filter(Boolean);
  const boardCards = [...boardView.querySelectorAll(".board-card")];
  const closedSections = [
    ...document.querySelectorAll("main.page > details.closed-section"),
  ];

  const listEmpty = document.createElement("p");
  listEmpty.className = "search-no-results";
  listEmpty.textContent = "没有匹配的事项";
  listEmpty.hidden = true;
  listView.appendChild(listEmpty);

  const boardEmpty = listEmpty.cloneNode(true);
  boardView.appendChild(boardEmpty);

  const statusOf = (node) => node.dataset.status || "";
  const corpusOf = (node) => node.dataset.search || node.textContent || "";

  const rememberOpen = (details) => {
    if (!details.hasAttribute("data-filter-was-open")) {
      details.dataset.filterWasOpen = details.open ? "true" : "false";
    }
  };

  const restoreOpen = (details) => {
    if (!details.hasAttribute("data-filter-was-open")) return;
    details.open = details.dataset.filterWasOpen === "true";
    details.removeAttribute("data-filter-was-open");
  };

  const childRowsOf = (row) => [
    ...row.querySelectorAll(":scope > td[colspan] > details .epic-children table.work-table > tbody > tr"),
  ];

  const workKey = (node) => {
    const link = node.querySelector("a.mono[href], a.epic-id[href]");
    const file = decodeURIComponent(link?.getAttribute("href") || "").split("/").pop() || "";
    return file.replace(/\.(?:html|md)$/, "").replace(/^TODO_/, "");
  };

  const recordsByKey = new Map();
  topRows.forEach((row) => {
    recordsByKey.set(workKey(row), {
      status: statusOf(row),
      corpus: corpusOf(row),
      children: childRowsOf(row).map((child) => ({
        status: statusOf(child),
        corpus: corpusOf(child),
      })),
    });
  });

  const selectedStatuses = () => activeStatuses.size === 0
    ? null
    : activeStatuses;

  const recordMatches = (record, tokens, statuses) => {
    const statusMatches = !statuses || statuses.has(record.status);
    return statusMatches && matches(record.corpus, tokens);
  };

  const reset = () => {
    topRows.forEach((row) => {
      row.hidden = false;
      childRowsOf(row).forEach((child) => {
        child.hidden = false;
      });
    });
    epicDetails.forEach(restoreOpen);
    boardCards.forEach((card) => {
      card.hidden = false;
    });
    closedSections.forEach((section) => {
      section.hidden = false;
      restoreOpen(section);
    });
    listEmpty.hidden = true;
    boardEmpty.hidden = true;
    refreshBoardCounts();
  };

  const refreshBoardCounts = () => {
    boardView.querySelectorAll(".board-col").forEach((column) => {
      const visible = [...column.querySelectorAll(":scope > .board-card")]
        .filter((card) => !card.hidden).length;
      const count = column.querySelector("h2 span");
      if (count) count.textContent = String(visible);
    });
  };

  const filterList = (tokens, statuses) => {
    let visibleCount = 0;
    topRows.forEach((row) => {
      const details = row.querySelector(":scope > td[colspan] > details");
      if (!details) {
        const visible = recordMatches(
          { status: statusOf(row), corpus: corpusOf(row) },
          tokens,
          statuses,
        );
        row.hidden = !visible;
        if (visible) visibleCount += 1;
        return;
      }

      rememberOpen(details);
      const parentMatches = recordMatches(
        { status: statusOf(row), corpus: corpusOf(row) },
        tokens,
        statuses,
      );
      const children = childRowsOf(row);
      const childMatches = children.map((child) => recordMatches(
        { status: statusOf(child), corpus: corpusOf(child) },
        tokens,
        statuses,
      ));
      const hasMatchingChild = childMatches.some(Boolean);
      const visible = parentMatches || hasMatchingChild;
      row.hidden = !visible;
      if (visible) visibleCount += 1;

      if (hasMatchingChild) {
        details.open = true;
        children.forEach((child, index) => {
          child.hidden = !childMatches[index];
        });
      } else {
        details.open = false;
        children.forEach((child) => {
          child.hidden = false;
        });
      }
    });
    return visibleCount;
  };

  const filterBoard = (tokens, statuses) => {
    let visibleCount = 0;
    boardCards.forEach((card) => {
      const record = recordsByKey.get(workKey(card)) || {
        status: statusOf(card),
        corpus: corpusOf(card),
        children: [],
      };
      const visible = recordMatches(record, tokens, statuses)
        || record.children.some((child) => recordMatches(child, tokens, statuses));
      card.hidden = !visible;
      if (visible) visibleCount += 1;
    });

    document.querySelectorAll("main.page > details.closed-section").forEach((section) => {
      rememberOpen(section);
      const visibleRows = [...section.querySelectorAll(":scope > .table-wrap > table.work-table > tbody > tr")]
        .filter((row) => !row.hidden);
      section.hidden = visibleRows.length === 0;
      if (visibleRows.length > 0) section.open = true;
    });
    refreshBoardCounts();
    return visibleCount;
  };

  const apply = () => {
    const query = normalize(searchInput.value);
    if (!query && activeStatuses.size === 0) {
      reset();
      return;
    }

    const tokens = query ? query.split(" ") : [];
    const statuses = selectedStatuses();
    const listVisible = filterList(tokens, statuses);
    const boardVisible = filterBoard(tokens, statuses);
    listEmpty.hidden = listVisible !== 0;
    boardEmpty.hidden = boardVisible !== 0 || listVisible !== 0;
  };

  const syncButtons = () => {
    filterButtons.forEach((button) => {
      const value = button.dataset.filter || "";
      const selected = value === "all" ? activeStatuses.size === 0 : activeStatuses.has(value);
      button.classList.toggle("active", selected);
      button.setAttribute("aria-pressed", String(selected));
    });
  };

  filterButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const value = button.dataset.filter || "";
      if (value === "all") {
        activeStatuses.clear();
      } else if (activeStatuses.has(value)) {
        activeStatuses.delete(value);
      } else {
        activeStatuses.add(value);
      }
      syncButtons();
      apply();
    });
  });

  searchInput.addEventListener("input", apply);
  searchInput.addEventListener("keydown", (event) => {
    if (event.key !== "Escape" || !searchInput.value) return;
    searchInput.value = "";
    apply();
  });
}
