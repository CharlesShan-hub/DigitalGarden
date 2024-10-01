---
dg-publish: true
dg-home: false
---
## Syntax

### 标题

```markdown
标题
# 一级标题
## 二级标题
### 三级标题
#### 四级标题

标题(另一种写法)
Heading level 1
===============
Heading level 2
---------------
```

### 段落与强调与引用

```markdown
段落
什么也不加就是段落，可以段落间空一行，就是加入段间距，也可以不空一行，就会取消段间距

强调
**bold text**
__bold text__
（👎 Love__is__bold，不要这样）
 *斜体*
（A*cat*meow,不要这样）
This text is ***really important***
This text is ___really important___.
This text is __*really important*__.
This text is **_really important_**.
This is really***very***important text.

引用
> 这是引用
>> 这是嵌套的引用
```

### 列表

```
列表
1. First item
2. Second item
3. Third item
4. Fourth item

列表可以不真正的排序
1. First item
1. Second item
1. Third item
1. Fourth item

甚至可以是错的
1. First item
8. Second item
3. Third item
5. Fourth item

加入 tab 可以进行缩进
1. First item
2. Second item
3. Third item
    1. Indented item
    2. Indented item
4. Fourth item

无序列表
- First item
- Second item
- Third item
- Fourth item

也可以用*
* First item
* Second item
* Third item
* Fourth item

或者*
+ First item
+ Second item
+ Third item
+ Fourth item
```

### 代码

````
单行代码
`print("Hello World!")`

多行代码
```python
a = 1
b = 2
a,b = b, a
```
````

### 分割线

```markdown
分割横线（注意前后要有空行）

***

---
_________________
```

### 各种链接

```markdown
图片
![Tux, the Linux mascot](/assets/images/tux.png)
![The San Juan Mountains are beautiful!](/assets/images/san-juan-mountains.jpg "San Juan Mountains")

超链接
My favorite search engine is [Google](https://www.google.com/，"Goto google").

带有链接的图片
[![An old rock in the desert](/assets/images/shiprock.jpg "Shiprock, New Mexico by Beau Rogers")](https://www.flickr.com/photos/beaurogers/31833779864/in/photolist-Qv3rFw-34mt9F-a9Cmfy-5Ha3Zi-9msKdv-o3hgjr-hWpUte-4WMsJ1-KUQ8N-deshUb-vssBD-6CQci6-8AFCiD-zsJWT-nNfsgB-dPDwZJ-bn9JGn-5HtSXY-6CUhAL-a4UTXB-ugPum-KUPSo-fBLNm-6CUmpy-4WMsc9-8a7D3T-83KJev-6CQ2bK-nNusHJ-a78rQH-nw3NvT-7aq2qf-8wwBso-3nNceh-ugSKP-4mh4kh-bbeeqH-a7biME-q3PtTf-brFpgb-cg38zw-bXMZc-nJPELD-f58Lmo-bXMYG-bz8AAi-bxNtNT-bXMYi-bXMY6-bXMYv)

URL 和 邮箱
<https://www.markdownguide.org>
<fake@example.com>
```

### 转义

```
如果要显示*，需要
\* 
其他的需要转义的符号：\`*_{}[]<>()#*+-/!|
```

## Links

* [Basic Syntax](https://www.markdownguide.org/basic-syntax/)