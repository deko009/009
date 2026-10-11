# BygoneMark.co · 业务规则表与站点地图

> 版本：2026-10-11 · 草案，等 BygoneMark 拍板
> 这份文件是全站数字和规则的**唯一依据**。Figma 里的每个价格、日期、起订量都按这里计算。规则一改，就按第四节的"受影响页面"同步修改。
> 标 ✅ 的规则已经按推荐方案写进 Figma；标 ❓ 的需要你们决定。

---

## 一、业务规则表

### R1 起订量 ✅
| 项 | 规则（已采用） | 备选 |
|---|---|---|
| 单品起订 | **每个产品 10 件**。同一产品的不同颜色、尺寸可以混合凑数 | 整单 10 件，不限单品（更宽松，但小批量生产成本高） |
| 复购 | 和首单一样，每个产品 10 件 | 复购最低 5 件（需要单独定价） |
| 套装 | 每个套装最少 10 套（每件单品都满 10） | — |
| 样品 | 每个产品 1 件，按零售价，60 天内下大货可抵扣 ❓ | 样品免费，但收运费 |

已修正：Onboarding 页的"一次 8 套"、案例页的"复购 8–15 套"、产品详情页单加 1 个笔插。现在都统一为 10 起。

### R2 阶梯价怎么计算 ✅
| 项 | 规则 |
|---|---|
| 档位 | 10–24 件 9 折 · 25–49 件 85 折 · 50 件以上 8 折 · 100 件以上单独报价 ❓（折扣本身仍待确认） |
| 计数单位 | **按单张订单的总件数**，所有产品合并计算 |
| 套装 | 1 套 = 2 件。**套装价按 25 套以上展示**，也就是 50 件以上、8 折档 |
| 年度累计 | **没有**。不按年累计，不保留历史档位 |
| 复购 | 和普通订单一样按件数计档，不继承上次的档位 |
| 价格展示 | 单品统一显示"**$X at 25+**"，零售价作为参考小字显示 |

已修正：
- 账户页删掉"2026 当前档位 15%"，改为"Logo 存档"
- 案例页删掉"12 个月保留档位"
- 全站 29 个套装价改为 8 折档
- 首页和产品总览的"零售价 + 85 折"改为直接显示 25 件价

### R3 Logo 制版费 ✅
- 整单**满 25 件免制版费**，10–24 件收一次 $X ❓
- 按"每个 Logo、每张订单"计算。复购沿用已存档的模具，不再收费

### R4 交期模型 ✅（数字待确认 ❓）
全站日期都按这个模型推算：

| 环节 | 时长 |
|---|---|
| 数字 proof | 收到 Logo 后 1 个工作日 |
| 生产 | proof 批准后 **7 个工作日**（暂定 ❓） |
| 地面运输 | 3–5 个工作日 |
| 从询价到收货 | 约 **12 个工作日** |
| 节日截单 | 10–99 件：11 月 20 日 → 12 月 15 日前到货（含感恩节 11/26–27 和缓冲时间）；100 件以上：11 月 1 日；加急：到 12 月 1 日 |

⚠️ 如果生产天数不是 7 天，以下内容都要重算：
- 询价第 1、3 步和提交成功页里的日期
- 案例时间线
- 场景页流程里的 "Days 3–9"
- 全站约 36 处"7 business days"
- 全站"12 days / 12 business days"

### R5 下单路径 ✅
| 路径 | 条件 | 去向 |
|---|---|---|
| 网上下单 | 10–49 件、寄到 1 个地址、标准个性化 | 订单清单 → **Check out**（刷卡或发票），付款后上传 Logo 和名单 |
| 询价 | 50 件以上、多地址、定制包装、用 PO 付款，或拿不准 | 订单清单 → **Request a quote**，或走询价表 |
| 批发 | 零售商转售 | 批发申请页 |

所有"加入"按钮统一为 **Add to order**，商品进入订单清单。

### R6 询价流程 ✅
- 第 1 步就收工作邮箱，用于保存进度、发送估价，防止中途流失
- "Send for a price now"：只填产品和数量就能提交，Logo、名单、地址之后再补
- 第 2、3 步可以"Skip for now"

### R7 渠道规则 ❓
- **.co 的批量价不高于 .net 的当期售价**：.net 搞促销时，.co 同步，或者在报价里按低价成交
- 推荐 .net 每个产品单笔限购 9 件，10 件以上引导到 .co
- **批发和企业批量的区别**：批发要提供转售证明（Resale certificate），商品不做个性化（店名定制除外），价格按 MSRP 折算。企业礼品走阶梯价，可以定制

### R8 主要行动 ✅
- 主行动只有一个：**Get a quote**（导航里的黑色按钮）
- 辅助入口：Bulk Pricing、Order list、预约通话、目录、预算工具。都不用黑色主按钮

---

## 二、站点地图（上线最小集 + 后续）

图例：✅ 已设计 · 🅿 设计了但建议上线后再开 · ⬜ 未设计 · 🗄 已归档

```
bygonemark.co
├─ 首页 ✅ 20:5
├─ Products  ✅ 135:135（总览）
│  ├─ Journals ✅ 59:26
│  ├─ Watch Cases ✅ 128:107
│  ├─ Small Leather Goods ✅ 165:495（书签 / 笔袋 / AirTag / 钱包 / 托盘）
│  │   └─ 🗄 旧页 Bookmarks / Pen Cases / Everyday Carry（y 33000，已合并）
│  ├─ Gift Sets ✅ 146:699（导航第 2 项）
│  └─ 产品详情页 ✅ 26:12（模板）＋ 订单清单抽屉 ✅ 166:510
├─ Solutions ✅ 135:482（总览）
│  ├─ Client Gifts ✅ 60:28
│  ├─ Employee Gifts ✅ 133:111
│  ├─ Holiday Gifts ✅ 133:391
│  ├─ New Hire Onboarding ✅ 133:671
│  ├─ Executive Gifts ✅ 133:951
│  ├─ Work Anniversaries ✅ 165:817（这一轮补上，之前是死链）
│  └─ 行业页：Law Firms ✅ 144:423
│      └─ Financial / Real estate / Tech / Consulting / Universities ⬜（上线前先指向 Solutions 总览的行业区）
├─ Customization ✅ 62:34
├─ Bulk Pricing ✅ 104:44
├─ Case Studies ✅ 112:61 → 案例详情 ✅ 114:65
├─ Resources ✅ 32:17 → 文章 ✅ 33:21
├─ 询价流程 ✅ 63:40 → 107:49 → 108:51 → 108:366 → 提交成功 108:701
├─ Company
│  ├─ About / Brand Facts ✅ 119:92
│  ├─ How It's Made ✅ 118:68（等真实照片）
│  ├─ Wholesale ✅ 110:57（只放在页脚和"三种下单方式"，不进主导航）
│  ├─ FAQ ✅ 121:99
│  └─ Contact ✅ 120:95
├─ 工具：Catalog 🅿 122:102 · Budget Planner 🅿 122:304
├─ 账户：Sign In ✅ 139:142 · Dashboard 🅿 139:244
├─ 政策：Shipping & Returns ✅ 137:139 · Terms ✅ 137:282 · Privacy ✅ 137:423（待法务审核）
├─ 搜索 ✅ 146:436 · 404 ✅ 146:574
└─ 手机版 ⬜
```

**统一后的分类：**
- 主导航：Products · Gift Sets · Solutions · Customization · Case Studies · Resources ｜ Bulk Pricing · Sign in · Order list ·【Get a quote】
- 页脚 Products 列：Journals · Watch Cases · Small Leather Goods · Gift Sets · Bulk Pricing · Catalog
- 页脚 Solutions 列：6 个场景（包括 Work Anniversaries）
- 行业固定 6 个：Law firms · Financial advisors · Real estate · Tech companies · Consulting firms · Universities。Bookstores 移到批发，不再算送礼行业

**产品数量 ❓：** 首页写 68 个，但设计稿里只放了有图有价的产品（Journals 29、Watch Cases 6、Small Leather Goods 10）。上线时要从 Shopify 实际上架数量自动读取，不要写死。

---

## 三、这一轮在 Figma 里改了什么

- 全站 41 个页面统一了交期：
  - 36 处"X business days"改为 7 个工作日
  - "9 business days"改为 12 个工作日
  - "Days 3–X"改为"Days 3–9"
  - 询价流程的日期按 11 月 20 日批准 proof 重算，12 月 8–10 日到货
- 29 个套装价按 8 折档重算，并保留到分：
  - 例如 Desk Set $68.72、Executive Set $207.12
  - 7 个场景页和行业页、Gift Sets、首页、Solutions 总览的预算区间同步更新
  - Holiday 页的 Executive Set 改名为 **The VIP Set**，避免和 $207.12 那个重名
- 按钮"Add to quote / Add set to quote"改为"Add to order"，共 20 个按钮和 17 处文字
- 导航：
  - Wholesale 换成 Gift Sets
  - 新增"Order list (0)"
  - 36 个页面同步
- 页脚：书签、笔袋、EDC 合并为 Small Leather Goods，新增 Gift Sets 和 Work Anniversaries
- 首页：删掉批发大区块；行业条里的 Bookstores 换成 Consulting firms
- 新增页面：
  - Small Leather Goods `165:495`
  - Work Anniversaries `165:817`
  - 订单清单抽屉 `166:510`
- 询价第 1 步加了工作邮箱和快速报价通道，第 2、3 步加了"Skip for now"
- 复购：统一为 10 套起，按件数计档，复购不用重新出 proof
- 账户页删掉了年度档位

---

## 四、规则改了要同步改哪里

| 规则变化 | 受影响页面 |
|---|---|
| 折扣比例 | Bulk Pricing 的价格表、所有"at 25+"价格、29 个套装价、预算工具、询价估价、订单清单、案例 |
| 生产天数 | 询价第 1、3 步和提交成功页、案例时间线、场景页流程、FAQ、政策页、首页和 Bulk Pricing 的交期列 |
| 起订量 | Bulk Pricing、FAQ、订单清单提示、所有"MOQ 10" |
| 制版费 | 首页价格表、产品详情页、定制页、Bulk Pricing |
| 套装展示档位 | 所有场景页、Gift Sets、搜索结果、首页预算区间 |
