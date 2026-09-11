# Jammers Simulator · 黑盒分析靶场

这是一个围绕 **Jammers-simulator-full-win64** 的本地靶场工程，用于学习 Windows 应用的文件取证、运行时观察、公开接口记录和可复现实验。靶场把模拟器当成一个**黑盒目标**：记录你在获授权的本地演练中能够合法观察到的输入、输出、计时和错误，不尝试读取隐藏场景或修改程序。

> **本仓库不重新分发官方模拟器二进制。** 原始安装目录约 679 MB，包含官方程序及 WebView2 运行时，且当前目录没有附带再分发许可。仓库只保存文件清单、SHA-256 校验值、启动脚本和分析记录模板。请从官方来源取得软件，并确认自己有权使用和保存它。

## 你会得到什么

```text
simulator/
  artifact-manifest.json       本地安装包的相对路径、大小和 SHA-256
  README.md                    如何挂载官方目录、哪些文件不入库
tools/
  inventory.py                 生成或校验本地安装目录清单
  launch_target.ps1            Windows 中显式启动目标程序
tests/
  test_manifest.py             清单结构和安全边界测试
docs/
  methodology.md               黑盒靶场方法、记录格式和禁止事项
  observations-template.md     单次观察记录模板
.github/workflows/ci.yml       只校验文档和清单，不启动 Windows 程序
```

靶场的目标是形成这样的证据链：

```text
官方来源文件夹
    → 清单与哈希校验
    → 明确的本地演练会话
    → 公开反馈/错误/计时记录
    → 可复核观察结论
```

## 快速开始

### 1. 准备官方目录

将你有权使用的 `Jammers-simulator-full-win64` 保留在本机，例如：

```text
C:\CUMCM\Jammers-simulator-full-win64
```

不要把 `JammersSimulatorData` 下的运行数据库、日志、账号信息或演练记录复制进 Git。当前样本中主程序的相对路径是：

```text
Jammers-simulator-full\jammers-simulator-full.exe
```

### 2. 校验本地样本

在仓库根目录运行：

```bash
python tools/inventory.py \
  --root "C:/CUMCM/Jammers-simulator-full-win64" \
  --manifest simulator/artifact-manifest.json \
  --verify
```

Windows PowerShell 使用同样的命令；路径可写成 `C:\CUMCM\Jammers-simulator-full-win64`。`--verify` 会检查主程序和 WebView2 运行时文件是否与当前清单一致；清单不包含用户数据目录。

### 3. 启动目标

仅在 Windows 中执行：

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\launch_target.ps1 `
  -SimulatorRoot 'C:\CUMCM\Jammers-simulator-full-win64' `
  -SessionLabel 'practice-20260912-01'
```

启动脚本只打开本地程序，不自动点击“正式测试”、不注入参数、不修改文件。模拟器页面若出现正式测试选项，保持停止状态；本项目的记录范围是你已获授权的演练会话。

## 分析范围

允许记录：

- 官方程序显示的版本、错误信息和公开帮助文本；
- 你自己启动的演练会话中的合法 API 反馈、动作顺序和虚拟计时；
- 本地文件的大小、哈希、签名状态和启动日志（先清理账号、路径和会话标识）；
- 在不改变程序和不读取隐藏状态的前提下，对观察结果做统计分析。

不在本靶场内做：

- 读取或导出隐藏源坐标、数量、发射方向、随机种子或内存对象；
- 解密官方加密日志、抓取受保护流量、绕过登录或正式/演练限制；
- 补丁、注入、修改可执行文件或借助调试器改变测试行为；
- 把账号、密码、`robot_id`、手机号、队伍信息或原始动作日志提交到公开仓库。

这些边界同时保护比赛公平性、第三方软件许可和你自己的账号安全。若目标是研究随机场景，应使用 `数学建模` 项目中的本地合成环境，或在靶场中只分析公开演练反馈。

## 记录与复现

每次观察复制 [记录模板](docs/observations-template.md)，为会话使用新的标签和新的输出目录。结论必须标注为：

- `observed`：界面或公开接口直接观察到；
- `inferred`：由多次观察推断，附样本量与不确定性；
- `unknown`：当前证据不足。

运行：

```bash
python -m pytest -q
```

CI 只运行清单和文档测试，永远不会下载或启动官方 Windows 程序。完整方法、数据字段和证据等级见 [docs/methodology.md](docs/methodology.md)。

## 来源与责任

本仓库是用户本地实验的组织层，不声称代表模拟器开发者，也不包含官方源代码。请从官方渠道获取最新程序并遵守竞赛规则、软件许可和当地法律；如果你没有再分发权，不要把二进制上传到 GitHub。发现清单不匹配时先停止分析，重新确认软件来源和版本。
