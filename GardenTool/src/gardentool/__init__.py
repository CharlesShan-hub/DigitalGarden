from pathlib import Path
import mistune
from bs4 import BeautifulSoup
import frontmatter
import shutil

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

    def sync(self,res_path):
        assert hasattr(self,'tree')
        # Get Res-dir path
        res_path = Path(res_path)
        assert res_path.exists()

        # move files
        if not Path(res_path,'.gitbook').exists():
            Path(res_path,'.gitbook').mkdir()
        if Path(res_path,'.gitbook/assets').exists():
            input(f"Going to delete {Path(res_path,'.gitbook/assets')}")
            input(f"Make sure")
            shutil.rmtree(Path(res_path,'.gitbook/assets'))
        shutil.copytree(Path(self.path, '.gitbook/assets'), Path(res_path, '.gitbook/assets'))

        # move main page
        with open(Path(self.path,'README.md'),'r') as f:
            file_md = f.read()
        post = frontmatter.loads(file_md)
        post['dg-home'] = True
        post['dg-publish'] = True
        updated_md = frontmatter.dumps(post)
        with open(Path(res_path,'README.md'), 'w+') as f:
            f.write(updated_md)

        # mkdir and check
        def move(base_path,key,value):
            if isinstance(value, str):
                p = Path(self.path,value)
                q = Path(res_path,value)
                if q.exists():
                    print('❌', q)
                else:
                    assert p.exists()
                    with open(p,'r') as f:
                        file_md = f.read()
                    post = frontmatter.loads(file_md)
                    post['dg-home'] = False
                    post['dg-publish'] = True
                    updated_md = frontmatter.dumps(post)
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
        