# Learning Log

这个项目现在是一个 **Markdown 写作 + GitHub 自动构建发布** 的静态博客。

你平时主要维护这些源文件：

- [content/home.md](E:\common\secondper.github.io\content\home.md)：首页介绍
- [content/about.md](E:\common\secondper.github.io\content\about.md)：关于页面
- [content/posts](E:\common\secondper.github.io\content\posts)：每一篇博客文章
- [content/site.json](E:\common\secondper.github.io\content\site.json)：博客名称、作者名、链接等配置
- [.github/workflows/pages.yml](E:\common\secondper.github.io\.github\workflows\pages.yml)：GitHub 自动构建与部署流程

站点当前信息：

- 作者：`Xie Chengdong`
- 博客名：`Chengdong's Notes`
- 邮箱：`xcd23@mail.ustc.edu.cn`
- GitHub：`https://github.com/secondper`

## 写新文章

在 `content/posts/` 里新建一个 Markdown 文件，建议文件名用：

```text
2026-04-29-my-new-post.md
```

文章开头保留这段元信息：

```md
---
title: 文章标题
date: 2026-04-29
tag: 标签
reading_time: 阅读 5 分钟
summary: 一句话摘要
---
```

后面直接写正文即可。

## 当前支持的 Markdown

- `#`、`##`、`###` 标题
- 普通段落
- `-` 无序列表
- `` `行内代码` ``
- 代码块
- Markdown 链接
- `**加粗**` 和 `*斜体*`

## 本地预览

如果你想在本地先看看效果：

```bash
python build.py
```

生成后可以直接打开：

- [index.html](E:\common\secondper.github.io\index.html)
- [archive.html](E:\common\secondper.github.io\archive.html)
- [about.html](E:\common\secondper.github.io\about.html)

## 日常发布流程

现在你不需要再把生成出来的 HTML 手动提交到 GitHub 了。

你以后通常只需要：

1. 修改 `content/` 里的 Markdown 或配置
2. 可选：本地运行 `python build.py` 预览
3. 提交并推送：

```bash
git add .
git commit -m "Add a new post"
git push
```

推送后，GitHub Actions 会自动：

1. 运行 `python build.py`
2. 生成 HTML 页面
3. 发布到 `https://secondper.github.io/`
