---
title: SEO、分享与产品分析
aliases: [SEO, Open Graph, OG, Umami, 网站统计, 合规]
tags: [fde, product, seo, analytics, sharing, compliance]
created: 2026-09-14
type: reference
domain: engineering
layer: foundation
canonical: false
status: active
updated: 2026-09-15
reviewed: 2026-09-20
stability: evergreen
sources: [https://opentelemetry.io/docs/]
---

# SEO、分享与产品分析

> [!abstract] 定位
> 能上线不等于能被找到，也不等于知道用户是否成功。本篇补上产品发布后的可发现性、社交分享、数据分析和基础合规。

## 一、SEO 基础三件套

### Metadata

每个重要页面至少有：

- 唯一 `<title>`。
- 清晰的 description。
- 合理的 canonical URL。
- 语言和 viewport 信息。

### Sitemap

列出希望搜索引擎抓取的规范 URL，发布新页面或删除页面时同步更新。

### Robots.txt

控制爬虫访问路径；不能把它当作保护敏感数据的安全机制，敏感内容必须依赖认证和权限。

Next.js 中把 metadata、`sitemap.ts`、`robots.ts` 纳入代码和部署检查。

## 二、内容与页面质量

- 标题准确描述页面，不堆关键词。
- URL 稳定、简短、可读。
- 内容回答真实问题，体现经验、证据和作者可信度。
- 图片有 alt，页面有清晰层级和内部链接。
- 页面速度、移动端体验和可访问性会影响用户和搜索表现。
- 需要时加入 JSON-LD 等结构化数据。

### Core Web Vitals 关注点

```text
LCP：主要内容出现多快
INP：交互响应多快
CLS：布局是否跳动
```

优化顺序优先于堆指标：

```text
关键渲染路径
→ 图片 / 字体 / 脚本加载
→ JavaScript 体积
→ 缓存和 CDN
→ 真实设备验证
```

## 三、Open Graph 与分享卡片

核心标签：

```html
<meta property="og:title" content="页面标题">
<meta property="og:description" content="页面摘要">
<meta property="og:image" content="https://example.com/og.png">
<meta property="og:url" content="https://example.com/page">
<meta property="og:type" content="website">
```

分享图片应：

- 在手机预览尺寸下仍可读。
- 有明确标题和品牌识别。
- 使用稳定、可公网访问的绝对 URL。
- 不包含未经授权的个人信息。

发布后用平台调试器和不同客户端验证缓存、裁切和中文显示。

## 四、Umami 与事件分析

基础指标：

- 访问量、访客数、会话数、跳出情况。
- 流量来源、设备、地区和入口页面。
- 关键事件：注册、上传、搜索、导出、邀请、付费。

```text
页面浏览 → 关键事件 → 完成任务
```

不要只追踪「访问量」这类虚荣指标；先定义产品成功行为，再设计事件。

隐私友好的分析原则：

- 只收集决策所需的数据。
- 不记录密码、Token 和原始敏感内容。
- 公开隐私说明和数据保留期限。
- 事件名和属性保持稳定，避免报表失效。

## 五、基础法律合规

根据用户地区和数据类型准备：

- 隐私政策：收集什么、为什么收集、保存多久、如何删除。
- 用户协议：服务范围、账号责任、内容和免责声明。
- Cookie / 分析说明。
- 面向欧盟用户时评估 GDPR 义务。
- 面向中国大陆提供服务时确认 ICP 备案和相关要求。

不要把 AI 生成的法律文本直接当作法律意见；高风险产品应让专业人士审核。

## 六、发布检查

- [ ] 每个公开页面有 metadata、canonical 和可抓取内容。
- [ ] sitemap、robots 和重定向正确。
- [ ] OG 图片在主要平台能正常显示。
- [ ] 已定义注册、激活、核心任务等事件。
- [ ] 统计脚本不会泄露密钥或敏感内容。
- [ ] 有隐私政策、用户协议和数据删除入口。
- [ ] 已确认目标地区的备案与合规要求。

相关笔记：

- [[Next.js]]
- [[部署方式]]
- [[Debugging 与可观测性]]
- [[用户反馈与产品迭代]]
- [[Web 用户认证与安全]]
