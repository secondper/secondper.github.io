# Learning Log

这个项目是一个 **Markdown 写作 + HTML 生成** 的静态博客。

你以后主要写这些源文件：

- [content/home.md](E:\common\secondper.github.io\content\home.md)：首页介绍
- [content/about.md](E:\common\secondper.github.io\content\about.md)：关于页面
- [content/posts](E:\common\secondper.github.io\content\posts)：每一篇博客文章
- [content/site.json](E:\common\secondper.github.io\content\site.json)：博客名称、作者名、链接等配置

站点当前已经替换为：

- 作者：`Xie Chengdong`
- 博客名：`Chengdong's Notes`
- 邮箱：`xcd23@mail.ustc.edu.cn`
- GitHub：`https://github.com/secondper`

## 写新文章

在 `content/posts/` 里新建一个 Markdown 文件，建议文件名用：

```text
2026-04-28-my-new-post.md
```

文件开头保留这段元信息：

```md
---
title: 文章标题
date: 2026-04-28
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

## 生成网站

在项目目录运行：

```bash
python build.py
```

生成后会更新：

- [index.html](E:\common\secondper.github.io\index.html)
- [archive.html](E:\common\secondper.github.io\archive.html)
- [about.html](E:\common\secondper.github.io\about.html)
- [posts](E:\common\secondper.github.io\posts) 下的文章 HTML

## 推荐工作流

1. 平时只写 `content/posts/*.md`
2. 写完后运行 `python build.py`
3. 双击 [index.html](E:\common\secondper.github.io\index.html) 预览
4. 后面再部署到 GitHub Pages

