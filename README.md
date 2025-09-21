# 华容道游戏2

这是华容道游戏的第二个版本，基于原版游戏复制而来。

## 项目结构

```
game2/
├── index.html              # 前端游戏页面
├── people.json             # 用户数据
├── origin.png              # 参考图片
├── split_images/           # 拼图块图片
├── worker/                 # Cloudflare Worker 后端
│   ├── src/
│   │   └── index.ts        # Worker 主文件
│   ├── schema.sql          # 数据库结构
│   ├── wrangler.toml       # Worker 配置
│   └── package.json        # 依赖配置
└── README.md               # 说明文档
```

## 部署步骤

### 1. 创建 Cloudflare D1 数据库

```bash
cd worker
npm install
wrangler d1 create game2_leaderboard
```

### 2. 创建 KV 命名空间

```bash
wrangler kv:namespace create CACHE
```

### 3. 更新配置文件

编辑 `worker/wrangler.toml`，填入真实的数据库ID和KV命名空间ID：

```toml
[[d1_databases]]
binding = "DB"
database_name = "game2_leaderboard"
database_id = "你的数据库ID"

[[kv_namespaces]]
binding = "CACHE"
id = "你的KV命名空间ID"
```

### 4. 运行数据库迁移

```bash
wrangler d1 execute game2_leaderboard --file=./schema.sql
```

### 5. 部署 Worker

```bash
wrangler deploy
```

### 6. 部署前端

将 `index.html`、`people.json`、`origin.png` 和 `split_images/` 目录上传到静态托管服务（如 Cloudflare Pages）。

## 配置说明

- **Worker URL**: `https://game2api.biboran.top` (需要替换为实际部署的URL)
- **前端域名**: `https://game2.biboran.top` (需要替换为实际部署的域名)
- **数据库**: `game2_leaderboard`
- **管理员密码**: `1314520`

## 功能特性

- 用户登录系统
- 3×3拼图游戏
- 实时计时和步数统计
- 排行榜系统
- 尝试次数限制（每用户最多3次）
- 管理后台

## 与原版游戏的区别

- 独立的数据库和KV存储
- 不同的Worker URL和域名配置
- 独立的用户数据文件
- 独立的游戏标题和标识



