## PyKnights  
PyKnights是一个为python语言提供代码高亮与提示功能的VSCode插件   
### 插件  
使用`pnpm run package`即可打包出VSIX文件 之后导入到VSCode即可  
### 测试  
如果希望不使用插件而调试程序的话可以在analyzer目录下运行  
建议首先创建虚拟环境 不过这一步是可选的  
```bash
conda create -n pyknights python=3.11
conda activate pyknights
```
安装依赖  
```bash
pip install -r requirements.txt
```
之后就可以直接运行python脚本了  
### 运行  
在analyzer目录下直接运行  
```bash
python main.py  
```
脚本带有命令行参数功能 可以通过添加`-h`参数查看帮助  