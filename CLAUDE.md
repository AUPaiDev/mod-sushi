# mod-sushi — Agent 工作流

苏轼 mod（`tauwoo.SuShiLegend`）采用四 agent 分工 + 主 Claude 总调度的开发模式。

## 四个专用 agent

| Agent | 模型 | 职责 | 工具白名单 |
|-------|------|------|-----------|
| `architect` | opus | 需求拆解 / 技术方案 / 任务派发清单 | 只读（Read/Grep/Glob/WebFetch/Skill） |
| `pixel-artist` | sonnet | 精灵图、肖像、行走动画（Python+Pillow） | Read/Write/Edit + 跑 python3 + 看图 |
| `coder` | sonnet | C# / JSON / i18n；编译验证 + 规范 commit | Read/Write/Edit/Bash（git/dotnet）+ Skill |
| `tester` | opus | build-deploy → launch → 日志 → 按验收点核查 | Read/Grep/Bash（含后台）；不 Edit/Write |

定义文件在 `.claude/agents/*.agent.md`。

## 主 Claude 的流程（强制）

```
① 明确需求 → ② 把守 git 闸口 → ③ 派 architect
                                     ↓
                           ④ 读方案，并行派 pixel-artist 与 coder
                                     ↓
                           ⑤ 问用户是否可启动游戏
                                     ↓
                           ⑥ 派 tester
                                     ↓
                           ⑦ 通过？→ 报告用户，由用户手动 merge
                              失败？→ 回 ③/④ 修，再 ⑥
```

### Git 规则（主 Claude 亲自执行）

1. 新任务开工前，由主 Claude 跑：
   ```bash
   /Users/tauwoo/.claude/plugins/cache/stardew-moddev/stardew-moddev-skills/1.0.0/scripts/git-sync.sh
   /Users/tauwoo/.claude/plugins/cache/stardew-moddev/stardew-moddev-skills/1.0.0/scripts/git-feature.sh <feature-name>
   ```
2. coder 在 feature 分支自行 commit（按 `git-commit-convention`）。
3. 画师交付的资产由**主 Claude 代为 commit**（scope: `assets` / `tools`）。
4. **push / merge 由用户手动操作**；任何 agent 和主 Claude 不得 push、merge、force-push、amend。
5. `build-deploy.sh` 内置 master 守卫，不要去绕它。

### 启动游戏前必须征得用户同意

tester 会真的弹出 Stardew Valley 窗口。主 Claude 每次派 tester 之前问一句：
> "准备好启动游戏测试了吗？（测试期间游戏窗口会占用前台）"

用户答 yes 才派 tester。

## agent 之间不互相调用

Claude Code 架构上只有主 Claude 能调 Agent 工具。四个 agent 的协作全部由主 Claude 串联：主 Claude 把 architect 的方案**完整转述**给 coder / pixel-artist / tester，不要让子 agent 自己去猜别人的输出。

## 常用路径备忘

- 项目根：`/Users/tauwoo/Documents/code/src/game/mod-sushi`
- 插件脚本根：`/Users/tauwoo/.claude/plugins/cache/stardew-moddev/stardew-moddev-skills/1.0.0/scripts`
- Steam Mods 目录：`/Users/tauwoo/Library/Application Support/Steam/steamapps/common/Stardew Valley/Contents/MacOS/Mods`
- 精灵图模板：`tools/generate_zhaoyun.py`（已跑通的完整参考）

## 不在 agent 流程内的事

- 纯咨询 / 读代码讲解 → 主 Claude 直接回
- 一行 typo / 重命名 → 主 Claude 直接改，不走四 agent
- 仅资产调色（不改规格）→ 可直接派 pixel-artist，跳过 architect
