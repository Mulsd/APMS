# AMPS管理系统
关于动画制作公司项目的管理系统解决方案。纯练手
使用了[element-plus-vite](https://github.com/element-plus/element-plus-vite-starter)启动项目

*注意：本项目AI含量极高。*欢迎各路大神优化。
## 开始使用
前端
```bash
npm install
npm run dev
```
后端
```python
pip install -r requirements.txt
#/backend
uvicorn main:app --reload
```
开启后端前需要编辑后端安全性配置
1.将.env.d重命名为.env
2.修改.env文件中关于数据库的数据
3.修改main.py文件中关于鉴权的数据
