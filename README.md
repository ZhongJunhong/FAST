由于本项目纯靠个人用爱发电，请勿过高期待，谢绝打赏。

# FAST: FindAllSciTool 把需要的文献尽可能找全

```python
import findallscitool as fast
pass
```

## 开发日志

### 20230123 更新

没有合适的可以获取abstract的api，所以对cited和citing的abstract和keywords的词频统计部分作罢，只对其统计author、affiliation、title、publication

向doi官网 https://www.doi.org/ 输入doi，会跳转到elsevier，然后再用爬虫将摘要爬取下来。

## 中文文档

包含以下基本功能：

1. 清洗元数据
   1. 使用正则表达式清洗从bibtex中读取的元数据。
   2. 给定DOI，补充缺失的元数据（不包含Abstract和Keywords）。若DOI缺失，则使用标题补充缺失的元数据。 
2. 给定文献，查找所有引用（cited）文献及其元数据（不包含Abstract和Keywords）。若DOI无法请求，则尝试使用标题请求，请求成功则修改原DOI，请求失败则跳过。
3. 给定文献，查找所有施引（citing）文献及其元数据（不包含Abstract和Keywords）。若DOI无法请求，则尝试使用标题请求，请求成功则修改原DOI，请求失败则跳过。
4. 补充缺失的Abstract和Keywords。
5. 词频统计，提取关键词及名词性短语，过滤常用词，提取和研究对象真正相关的内容。
6. 下载pdf（暂支持英文）。
7. 更多功能尽请期待。

## English Documentation
后续补充 