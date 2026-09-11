# 本地模拟器样本

此目录只保存**非二进制元数据**。官方 Windows 安装目录不进入 Git：主目录约 679 MB，包含 `jammers-simulator-full.exe` 与 WebView2Runtime。使用仓库根目录的 `tools/inventory.py` 生成或校验清单。

```powershell
python tools/inventory.py `
  --root 'C:\CUMCM\Jammers-simulator-full-win64' `
  --manifest simulator/artifact-manifest.json `
  --verify
```

`JammersSimulatorData` 中的 SQLite、启动日志和会话输出属于本机运行状态，不纳入公开清单。清单中的路径均相对于安装包根目录；哈希仅用于确认你分析的是同一个本地样本，不代表官方发布签名。
