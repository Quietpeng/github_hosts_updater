# GitHub Hosts Updater

## 项目简介
这是一个自动更新 GitHub Hosts 配置的工具，通过定期从可靠源获取最新的 hosts 配置，帮助用户在中国大陆更流畅地访问 GitHub。

作者: [Quietpeng](https://github.com/Quietpeng)
地区: China

## 特别感谢
- hosts数据来源: [GitHub520](https://github.com/521xueweihan/GitHub520)
- 默认更新地址: https://raw.hellogithub.com/hosts

## 功能特点
- 自动从可靠源获取最新的 GitHub hosts 配置
- 图形界面操作，使用简单
- 后台自动更新，无需手动干预
- 安全可靠，代码开源透明
- 支持自定义hosts更新源

## 使用说明
1. 确保以管理员权限运行程序
2. 启动程序后会显示功能说明和安全提示
3. 确认后程序会在后台运行，每10分钟自动更新一次hosts文件
4. 程序运行时请勿关闭窗口

## 注意事项
- 本程序需要修改系统hosts文件，请确保有管理员权限
- 修改hosts文件可能带来潜在风险，请从可信源获取程序
- 程序运行时会在后台持续运行，如需停止请手动关闭窗口

## 技术架构
- 使用Python开发
- 使用tkinter构建图形界面
- 使用requests处理网络请求
- 使用os模块处理文件操作



## 许可证
MIT License 