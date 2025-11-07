# 🎵 AI Music BGM Auto-Generator for YouTube

睡眠導入・作業用BGM動画を自動生成し、YouTubeで収益化するための総合ツールキット

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## 🌟 特徴

- 🎨 **21種類のテンプレート**：ノイズ系・自然音・ピアノ等
- 🤖 **半自動モード**：API費用$0（月$14のみ）
- 📋 **チェックリスト機能**：進捗を可視化
- 🎬 **ロング/ショート対応**：長尺・YouTube Shorts両対応
- 📤 **YouTube自動アップロード**：ワンクリックで投稿
- 💰 **月$14で運用可能**：API呼び出し不要

---

## 📁 プロジェクト構成

```
├── templates/              21種類のBGMテンプレート
│   ├── noise/             ピンク/ホワイト/ブラウンノイズ
│   ├── nature/            雨音・森・海など
│   ├── fire/              焚き火・温かみ系
│   ├── piano/             ピアノ・子守歌
│   ├── ambient/           アンビエント・ドローン
│   └── special/           ASMR・特殊音源
│
├── automation/             自動化ツール
│   ├── manual.bat         半自動モードGUI起動
│   ├── setup.bat          初回セットアップ
│   ├── manual_mode_v2.py  GUIアプリケーション
│   └── modules/           処理モジュール
│
└── docs/                   ドキュメント
    ├── 戦略.md            収益化戦略・KPI
    └── テンプレート.md    共通フォーマット
```

---

## 🚀 クイックスタート

### 1. リポジトリをクローン

```bash
git clone https://github.com/YOUR_USERNAME/sleep-bgm-automation.git
cd sleep-bgm-automation
```

### 2. セットアップ

```bash
cd automation
setup.bat  # Windows
# または python setup.py  # Mac/Linux
```

### 3. YouTube API認証

1. [Google Cloud Console](https://console.cloud.google.com/)でプロジェクト作成
2. YouTube Data API v3を有効化
3. `credentials.json`をダウンロードして`automation/`に配置
4. `auth.bat`実行

### 4. 動画作成

```bash
manual.bat
```

GUIが起動します：
1. テンプレート選択
2. プロンプトをMubertにコピー
3. Mubertで音源生成（手動）
4. ダウンロードした音源を追加
5. 「生成＋アップロード」をクリック

---

## 💰 費用

### 半自動モード（推奨）
- **Mubert Creator/Pro**: $14/月
- **API呼び出し**: $0
- **合計**: **$14/月**

### 完全自動モード
- **Mubert**: $14/月
- **API呼び出し**: $20〜$40/月
- **合計**: $34〜$54/月

---

## 📋 テンプレート一覧

| カテゴリ | テンプレート数 | 例 |
|---------|--------------|-----|
| 🔊 ノイズ系 | 3 | ピンクノイズ、ホワイトノイズ |
| 🌿 自然音 | 6 | 雨音、森、海辺 |
| 🔥 焚き火系 | 2 | 炎、雨焚火 |
| 🎹 ピアノ系 | 4 | ピアノ、子守歌 |
| 🌌 アンビエント | 3 | ドローン、シータ波 |
| ✨ 特殊 | 3 | ASMR、ささやきガイド |

**合計**: 21種類

すべてのテンプレートは60 BPM指定のMubertプロンプト付き

---

## 🎯 収益化目標

### 2ヶ月目
- 登録者: 1,000人
- 総再生時間: 4,000時間
- → **YouTube収益化達成**

### 6ヶ月目
- 月間収益: $500+

### 12ヶ月目
- 月間収益: $3,000+

詳細: [docs/戦略.md](docs/戦略.md)

---

## 📖 ドキュメント

- [QUICKSTART.md](automation/QUICKSTART.md) - 5分で始める
- [使い方.txt](automation/使い方.txt) - 重要事項
- [戦略.md](docs/戦略.md) - 収益化戦略
- [今すぐ始める.txt](今すぐ始める.txt) - 最短ガイド

---

## 🛠️ 技術スタック

- **Python 3.10+**
- **Tkinter** (GUI)
- **MoviePy** (動画生成)
- **Pydub** (音声編集)
- **Google API** (YouTube)
- **Mubert** (音源生成 - 手動)

---

## ⚠️ 重要な注意事項

### API使用について
- 半自動モードは**Mubert APIを使用しません**
- YouTube Data APIのみ使用（無料枠内）
- 音源はMubertサイトで手動生成

### ライセンス
- 音源: Mubert Creator/Proプラン（商用利用許諾）
- コード: MIT License

---

## 🤝 コントリビューション

Issues、Pull Requestsを歓迎します！

---

## 📜 ライセンス

MIT License - 詳細は[LICENSE](LICENSE)を参照

---

## 🙏 謝辞

- [Mubert](https://mubert.com/) - AI音楽生成
- [MoviePy](https://zulko.github.io/moviepy/) - 動画処理
- [Pydub](https://github.com/jiaaro/pydub) - 音声処理

---

**Star⭐していただけると励みになります！**

