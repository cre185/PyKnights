const shell = require('shelljs');

// 创建 Python 虚拟环境
if (shell.exec('python -m venv env').code !== 0) {
  shell.echo('Error: Python venv failed');
  shell.exit(1);
}

// 安装 Python 依赖
if (shell.exec('env\\Scripts\\pip install -r requirements.txt').code !== 0) {
  shell.echo('Error: pip install failed');
  shell.exit(1);
}