# 普信债流动性数据可视化

## 使用方法

### 更新数据（每周）
1. 将最新的 Excel 文件重命名为 `data.xlsx`，替换本目录下的 `data.xlsx`
2. 双击 **`一键更新.bat`**
3. 等待 2-3 分钟，网站自动更新

### 网站地址
https://cayinc.github.io/puxin-bond-liquidity/

### 构建流程
```
data.xlsx → build_data.py → page_data.json → build_page.py → index.html
```

GitHub Actions 会在每次 push 后自动运行上述构建流程，无需本地执行。

## 项目结构
```
├── data.xlsx              # 数据源（需手动替换更新）
├── build_data.py          # 解析 Excel → JSON
├── build_page.py          # JSON → 内嵌数据的 HTML
├── index.html             # 最终网页（自动生成，不要手动编辑）
├── 一键更新.bat            # 双击即可 push 到 GitHub
├── .github/workflows/
│   └── build.yml          # GitHub Actions 自动构建配置
└── README.md
```

## 注意事项
- Excel 文件格式和 Sheet 结构必须保持一致
- 仅修改 `data.xlsx`，不要修改脚本文件
- 如果 GitHub Actions 构建失败，检查 Actions 页面的错误日志
