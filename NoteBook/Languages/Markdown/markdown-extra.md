---
dg-publish: true
dg-home: false
---
## Syntax

### 表格

```markdown
表格
| Syntax      | Description |
| ----------- | ----------- |
| Header      | Title       |
| Paragraph   | Text        |

表格可以不用这么工整
| Syntax      | Description |
| --- | --------- |
| Header | Title |
| Paragraph | Text  |

表格对齐
| Syntax      | Description | Test Text     |
| :---        |    :----:   |          ---: |
| Header      | Title       | Here's this   |
| Paragraph   | Text        | And more      |

表格中显示|，需要用&#124;
```

### 脚注

（就是论文中的\[1]\[2])

```
Here's a simple footnote,[^1] and here's a longer one.[^bignote]

[^1]: This is the first footnote.

[^bignote]: Here's one with multiple paragraphs and code.

    Indent paragraphs to include them in the footnote.

    `{ my code }`

    Add as many paragraphs as you like.
```

### 内部跳转

```markdown
首先要在内部生成 ID

### My Great Heading {#custom-id}

然后链接链到 ID

[Heading IDs](#heading-ids)
```

### Definition List

这样就是First Term和Second Term分成两大块，内部没有空行的

```markdown
First Term
: This is the definition of the first term.

Second Term
: This is one definition of the second term.
: This is another definition of the second term.
```

### 删除

```markdown
~~The world is flat.~~ We now know that the world is round.
```

### task list

```markdown
- [x] Write the press release
- [ ] Update the website
- [ ] Contact the media
```

### emoji

```markdown
Gone camping! :tent: Be back soon.

That is so funny! :joy:
```

Gone camping! ⛺ Be back soon.

That is so funny! 😂

### Highlight <a href="#highlight" id="highlight"></a>

```
I need to highlight these ==very important words==.
```

I need to highlight these <mark style="background-color:red;">very important words</mark>.

### Subscript <a href="#subscript" id="subscript"></a>

```
H~2~O
```

$$
H_2O
$$

like this： H\<sub>2\</sub>O

### Superscript <a href="#superscript" id="superscript"></a>

```
X^2^
```

$$
x^2
$$

like this：X\<sup>2\</sup>

### Automatic URL Linking <a href="#automatic-url-linking" id="automatic-url-linking"></a>

会直接带上超链接

```markdown
http://www.example.com
```

### Disabling Automatic URL Linking <a href="#disabling-automatic-url-linking" id="disabling-automatic-url-linking"></a>

不要Automatic URL Linking

```
`http://www.example.com`
```

## Links

* [https://michelf.ca/projects/php-markdown/extra/](https://michelf.ca/projects/php-markdown/extra/)\
* [https://www.markdownguide.org/extended-syntax/](https://www.markdownguide.org/extended-syntax/)
