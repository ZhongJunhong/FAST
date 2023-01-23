由于本项目纯靠个人用爱发电，请勿过高期待，谢绝打赏。

# FAST: FindAllSciTool 把需要的文献尽可能找全

## Quick Start

```python
import findallscitool as fast
pass
```

## 开发日志

### 20230123 更新

没有合适的可以获取abstract的api，所以对cited和citing的abstract的词频统计部分作罢，只对其统计author、affiliation、title、publication

向doi官网 https://www.doi.org/ 输入doi，会跳转到elsevier，然后再用爬虫将摘要爬取下来


## 中文文档

把需要的文献尽可能找全。

包含以下基本功能：

1. 给定文献，查找所有引用（cited）文献。
2. 给定文献，查找所有施引（citing）文献。
3. 给定DOI，查找元数据。
4. 词频统计，提取关键词。
5. 下载pdf（暂支持英文）。
6. 更多功能尽请期待。


## English Documentation
