# findallscitool



# 开发日志
get_ref_cite.py写好了：
1. 从bibtex文件获取doi_list
2. 从doi_list获取cited和citing
3. 对所有doi进行去重

但由于没有合适的可以获取abstract的api，所以对cited和citing的abstract的词频统计部分作罢，只对其统计author、affiliation、title、publication
还有个方法，向doi官网 https://www.doi.org/ 输入doi，会跳转到elsevier，然后再用爬虫将摘要爬取下来


# FindAllSciTool

## Quick Start

```python
import findallscitool as fast
pass
```

## 中文文档



## English Documentation
