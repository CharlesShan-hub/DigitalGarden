import re

# 示例HTML
html_input = '''
<figure><img src="../../.gitbook/assets/image (84).png" alt="" width="375"><figcaption><p>abcd</p></figcaption></figure>
<figure><img src="www.baidu.com/image (84).png" alt="" width="375"><figcaption><p>abcd</p></figcaption></figure>
abcd,something others
<figure><img src="../../.gitbook/assets/image (45).png" alt="" width="375"><figcaption></figcaption></figure>
'''

# 由于示例HTML包含<figure>和<figcaption>标签，我们需要进一步处理
# 正则表达式匹配<figure>标签内的内容，并捕获img标签和figcaption内容
figure_pattern = re.compile(r'<figure><img\s+src="(.*?)"(.*?)><figcaption>(?:<p>)?(.*?)(?:</p>)?</figcaption></figure>')
# 使用嵌套的替换函数处理整个<figure>标签
markdown_output = figure_pattern.sub(lambda m: f"""![[{m.group(1) if m.group(1).find('.gitbook/')==-1 else m.group(1)[m.group(1).find('gitbook/'):]}]]{m.group(3)}""", html_input)

# 打印转换后的Markdown文本
print(markdown_output)
