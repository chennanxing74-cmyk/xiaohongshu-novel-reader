@echo off
echo 🚀 Spider项目推送到GitHub
echo ================================

echo 📋 推送信息:
echo    仓库: spider-novel-reader
echo    用户: chennanxing74-cmyk
echo    分支: main

echo.
echo ⚠️  请确保已在GitHub创建仓库:
echo    https://github.com/new
echo    仓库名: spider-novel-reader
echo    设置为Public，不要初始化任何文件

echo.
pause

echo 🔄 开始推送...
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ 推送成功！
    echo.
    echo 📋 接下来请:
    echo 1. 进入GitHub仓库设置
    echo 2. 启用GitHub Pages
    echo 3. 等待部署完成
    echo.
    echo 🌐 部署后访问:
    echo    主页: https://chennanxing74-cmyk.github.io/spider-novel-reader/
    echo    阅读器: https://chennanxing74-cmyk.github.io/spider-novel-reader/xiaohongshu_app/
) else (
    echo.
    echo ❌ 推送失败！
    echo.
    echo 💡 可能的解决方案:
    echo 1. 确保GitHub仓库已创建
    echo 2. 检查网络连接
    echo 3. 配置Git认证信息
    echo 4. 使用GitHub Desktop推送
)

echo.
pause
