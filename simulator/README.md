# 本地模拟器样本

此目录包含完整的 `Jammers-simulator-full-win64` Windows 样本，约 679 MB；大文件通过 Git LFS 管理。`artifact-manifest.json` 保存程序与运行时清单，`full-artifact-manifest.json` 保存 272 个文件的完整清单（含运行状态）。若使用其他样本，运行仓库根目录的 `tools/inventory.py` 生成或校验清单。

```powershell
python tools/inventory.py `
  --root 'C:\CUMCM\Jammers-simulator-full-win64' `
  --manifest simulator/artifact-manifest.json `
  --verify
```

`JammersSimulatorData` 中的 SQLite、启动日志和会话输出随完整样本保留；它们不纳入 `artifact-manifest.json`，但会出现在 `full-artifact-manifest.json`。清单中的路径均相对于安装包根目录；哈希仅用于确认样本一致，不代表官方发布签名。
