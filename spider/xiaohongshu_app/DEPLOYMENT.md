# GitHub Pages 部署说明

## 🚀 快速部署

### 1. 创建GitHub仓库
1. 访问 https://github.com/new
2. 仓库名称：`xiaohongshu-novel-reader`
3. 设置为Public
4. 不要初始化README、.gitignore或license

### 2. 上传代码
```bash
# 在项目目录中执行
git init
git add .
git commit -m "Initial commit: 小红书风格小说阅读器"
git branch -M main
git remote add origin https://github.com/chennanxing74-cmyk/xiaohongshu-novel-reader.git
git push -u origin main
```

### 3. 启用GitHub Pages
1. 进入仓库设置页面
2. 滚动到"Pages"部分
3. Source选择"Deploy from a branch"
4. Branch选择"main"
5. 文件夹选择"/ (root)"
6. 点击Save

### 4. 访问网站
等待几分钟后，访问：
https://chennanxing74-cmyk.github.io/xiaohongshu-novel-reader/

## 🔧 自定义配置

### 修改GitHub用户名
1. 编辑 `deploy_to_github.py`
2. 修改 `github_username` 变量
3. 重新运行脚本

### 自定义域名
1. 在仓库根目录创建 `CNAME` 文件
2. 文件内容为你的域名，如：`novel.yourdomain.com`
3. 在域名DNS设置中添加CNAME记录指向 `chennanxing74-cmyk.github.io`

### 自动部署
项目已配置GitHub Actions，推送到main分支会自动部署。

## 📱 PWA安装

部署后，用户可以将网站安装为APP：

### Android/Chrome
1. 访问网站
2. 浏览器会显示"添加到主屏幕"提示
3. 点击安装

### iOS/Safari
1. 访问网站
2. 点击分享按钮
3. 选择"添加到主屏幕"

## 🛠️ 故障排除

### 页面404错误
- 检查仓库是否为Public
- 确认GitHub Pages已启用
- 等待几分钟让部署完成

### 样式或脚本加载失败
- 检查文件路径是否正确
- 确认所有文件都已上传

### PWA功能不工作
- 确认网站使用HTTPS访问
- 检查Service Worker是否正确注册
- 查看浏览器控制台错误信息

## 📞 获取帮助

如遇问题，请：
1. 检查GitHub Pages部署状态
2. 查看浏览器控制台错误
3. 提交Issue到项目仓库

---

**祝您部署成功！** 🎉
