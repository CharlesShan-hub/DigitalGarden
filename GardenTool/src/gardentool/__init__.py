from pathlib import Path
import mistune
from bs4 import BeautifulSoup
import frontmatter
import shutil
import re
import os

def modify(html):
    # 使用正则表达式匹配图片标签和对应的标题标签
    img_pattern = r'<img src="(?P<src>[^"]+)" alt="" width="\d+">'
    figcaption_pattern = r'<figcaption><p>\[(?P<caption>\d+)\]</p></figcaption>'

    # 查找图片路径和标题
    img_match = re.search(img_pattern, html)
    figcaption_match = re.search(figcaption_pattern, html)

    if img_match and figcaption_match:
        # 提取图片路径和标题
        img_src = img_match.group('src')
        index = img_src.find("gitbook/")
        img_src = img_src[index:] if index != -1 else img_src
        caption = figcaption_match.group('caption')
        # 构造markdown格式的字符串
        markdown = f"![[{img_src}]]([{caption}])"
        return markdown
    else:
        return html

class Converter:
    def __init__(self):
        pass
    
    def load(self,path):
        # Get Tree file path
        self.path = Path(path)
        tree_path = Path(self.path,"SUMMARY.md")
        assert tree_path.exists()

        # Get Tree file content (markdown)
        with open(tree_path,'r') as tree:
            tree_md = tree.read()
        
        # Get Tree file content (html)
        tree_html = mistune.html(tree_md)
        soup = BeautifulSoup(tree_html, 'html.parser')

        # Get Tree dict
        temp_dict = {}
        all_h = soup.find_all(['h1','h2'],recursive=False)
        all_ul = soup.find_all('ul',recursive=False)
        all_h.pop(0)
        all_ul.pop(0)
        for (key,value) in zip(all_h,all_ul):
            temp_dict[key.text] = value

        # Complete Tree dict 
        def _build_tree(node):
            d = {}
            for n in node.find_all('li',recursive=False):
                a = n.find('a')
                assert a is not None
                if n.find('ul') is None:
                    d[a.text] = a['href']
                else:
                    d[a.text] = [a['href'],_build_tree(n.find('ul'))]
            return d
        self.tree = {}
        for (k,v) in temp_dict.items():
            self.tree[k] = _build_tree(v)
    
    def check(self,res_path):
        assert hasattr(self,'tree')
        # Get Res-dir path
        res_path = Path(res_path)
        assert res_path.exists()

        # mkdir and check
        def check(base_path,key,value):
            if isinstance(value, str):
                p = Path(res_path,value)
                assert Path(self.path,value).exists()
                if p.exists():
                    marker = '❌' # Need Update
                elif not p.exists():
                    marker = '✅' # Only Copy
                print(marker, p)

            elif isinstance(value, dict):
                p = Path(base_path,key.lower().replace(' ','-'))
                if not p.exists():
                    p.mkdir()
                for (k,v) in value.items():
                    check(p,k,v)
            elif isinstance(value, list):
                p = Path(base_path,key.lower().replace(' ','-'))
                if not p.exists():
                    p.mkdir()
                check(p,key,value[0])
                for (k,v) in value[1].items():
                    check(p,k,v)
            else:
                raise TypeError(f'value shuold only be list, set or str not {type(value)}')
        for (k,v) in self.tree.items():
            check(res_path,k,v)

    def sync(self,res_path,cover):
        assert hasattr(self,'tree')
        # Get Res-dir path
        res_path = Path(res_path)
        assert res_path.exists()

        # move files
        if not Path(res_path,'gitbook').exists():
            Path(res_path,'gitbook').mkdir()
        if Path(res_path,'gitbook/assets').exists():
            input(f"Going to delete {Path(res_path,'gitbook/assets')}")
            input(f"Make sure")
            shutil.rmtree(Path(res_path,'gitbook/assets'))
        shutil.copytree(Path(self.path, '.gitbook/assets'), Path(res_path, 'gitbook/assets'))

        # move main page
        with open(Path(self.path,'README.md'),'r') as f:
            file_md = f.read()
        post = frontmatter.loads(file_md)
        post['dg-home'] = False
        post['dg-publish'] = True
        updated_md = frontmatter.dumps(post)
        with open(Path(res_path,'README.md'), 'w+') as f:
            f.write(updated_md)

        # move tree page
        with open(Path(self.path,'SUMMARY.md'),'r') as f:
            file_md = f.read()
        post = frontmatter.loads(file_md)
        post['dg-home'] = True
        post['dg-publish'] = True
        updated_md = frontmatter.dumps(post)
        # 正则表达式匹配Markdown链接格式，并捕获链接文本和URL
        markdown_link_pattern = re.compile(r"\[(.*?)\]\((.*?)\.md\)")
        # 替换链接格式
        updated_md = markdown_link_pattern.sub(lambda m: f"{m.group(1)}: [[{m.group(2)}|{os.path.basename(m.group(2))}]]", updated_md)
        with open(Path(res_path,'SUMMARY.md'), 'w+') as f:
            f.write(updated_md)

        # mkdir and check
        def move(base_path,key,value):
            if isinstance(value, str):
                p = Path(self.path,value)
                q = Path(res_path,value)
                if not cover:
                    if q.exists():
                        print('❌', q)
                        return
                assert p.exists()
                with open(p,'r') as f:
                    file_md = f.read()
                post = frontmatter.loads(file_md)
                post['dg-home'] = False
                post['dg-publish'] = True
                post['dg-permalink'] = value
                updated_md = frontmatter.dumps(post)
                # 由于示例HTML包含<figure>和<figcaption>标签，我们需要进一步处理
                # 正则表达式匹配<figure>标签内的内容，并捕获img标签和figcaption内容
                figure_pattern = re.compile(r'<figure><img\s+src="(.*?)"(.*?)><figcaption>(?:<p>)?(.*?)(?:</p>)?</figcaption></figure>')
                # 使用嵌套的替换函数处理整个<figure>标签
                updated_md = figure_pattern.sub(lambda m: f"""![[{m.group(1) if m.group(1).find('.gitbook/')==-1 else m.group(1)[m.group(1).find('gitbook/'):]}]]{m.group(3)}""", updated_md)

                # 正则表达式匹配<img>标签，并捕获src和alt属性
                img_tag_pattern = re.compile(r'<img\s+src="([^"]+)"\s+alt="([^"]*)".*?>')
                # 替换<img>标签为Obsidian链接格式，并处理.gitbook路径
                updated_md = img_tag_pattern.sub(lambda m: f"![[{m.group(1).replace('.gitbook', 'gitbook')}]]{m.group(2)}", updated_md)
                with open(q, 'w+') as f:
                    f.write(updated_md)

            elif isinstance(value, dict):
                p = Path(base_path,key.lower().replace(' ','-'))
                if not p.exists():
                    p.mkdir()
                for (k,v) in value.items():
                    move(p,k,v)
            elif isinstance(value, list):
                p = Path(base_path,key.lower().replace(' ','-'))
                if not p.exists():
                    p.mkdir()
                move(p,key,value[0])
                for (k,v) in value[1].items():
                    move(p,k,v)
            else:
                raise TypeError(f'value shuold only be list, set or str not {type(value)}')
        for (k,v) in self.tree.items():
            move(res_path,k,v)
    
    def add(self,res_path):
        self.sync(res_path,cover=False)

    def cover(self,res_path):
        self.sync(res_path,cover=True)
  