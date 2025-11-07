# 🎵 YouTube睡眠・作業用BGM自動生成ツール

**月$14だけ**で、YouTube収益化を目指せる AI音楽BGM自動生成システム

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Mubert](https://img.shields.io/badge/Mubert-Creator%2FPro-green)](https://mubert.com/render/pricing?via=1cc55b)

> 💡 テンプレート選択 → プロンプトコピー → Mubertで生成 → ワンクリックでYouTubeアップロード！

<p align="center">
  <img src="https://img.shields.io/badge/Templates-21%E7%A8%AE%E9%A1%9E-blue" alt="Templates">
  <img src="https://img.shields.io/badge/Cost-$14%2Fmonth-green" alt="Cost">
  <img src="https://img.shields.io/badge/API-No%20Cost-brightgreen" alt="API">
</p>

---

## 🌟 このツールでできること

### 💰 最小コストで収益化
- **月額$14のみ**でYouTube BGMチャンネル運営
- Mubert API呼び出し不要（手動生成で節約）
- 完全自動モードより**月$20〜$40安い**

### 🎨 豊富なテンプレート
- **21種類**のBGMテンプレート（カテゴリ別）
- すべて60 BPM指定のMubertプロンプト付き
- タイトル・タグ・カラーパレットも完備

### 🖥️ 使いやすいGUI
- チェックリスト機能で進捗管理
- テンプレート選択→プロンプト自動表示
- Mubertサイトへワンクリック
- ドラッグ&ドロップで音源追加

### 📹 動画形式
- **ロング動画**：25分〜10時間（睡眠・作業用）
- **ショート動画**：60秒（YouTube Shorts）
- **変換機能**：ロングからショートへ切り出し

### 🚀 自動化機能
- 音声編集（フェード・結合）自動
- 動画生成自動
- YouTube アップロード自動
- メタデータ（タイトル・説明・タグ）自動生成

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

## 🚀 5分で始める

### 📦 1. インストール

```bash
git clone https://github.com/suyako-teck/sleep-bgm-automation.git
cd sleep-bgm-automation/automation
setup.bat
```

### 🔐 2. Mubert登録

[**→ Mubert Creator登録（$14/月）**](https://mubert.com/render/pricing?via=1cc55b)

> 💝 このリンクから登録すると開発をサポートできます（30%還元）

### 🎥 3. YouTube API設定

1. [Google Cloud Console](https://console.cloud.google.com/)
2. YouTube Data API v3を有効化
3. `credentials.json`をダウンロード→`automation/`に配置
4. `auth.bat`実行

### 🎬 4. 初めての動画作成

```bash
manual.bat
```

**GUIの使い方：**

<table>
<tr>
<td width="50%">

**左側：チェックリスト**
- ✅ 進捗が一目でわかる
- 次のステップを表示

</td>
<td width="50%">

**中央：テンプレート選択**
- 6カテゴリ・21種類
- プロンプト自動表示

</td>
</tr>
<tr>
<td colspan="2">

**右側：設定＋実行**
- タイトル入力
- ロング/ショート選択
- ワンクリックで生成＋アップロード

</td>
</tr>
</table>

### ✨ 操作の流れ

```
1. テンプレート選択（例：ピンクノイズ）
   ↓
2. 📋 プロンプトコピー
   ↓
3. 🌐 Mubert開く → 音源生成（10分）
   ↓
4. 音源をダウンロード
   ↓
5. GUIで「音源追加」
   ↓
6. 🚀 生成＋アップロード（60分）
   ↓
7. ✅ YouTube投稿完了！
```

---

## 💰 費用

### 半自動モード（推奨）
- **Mubert Creator/Pro**: $14/月 → [**登録はこちら**](https://mubert.com/render/pricing?via=1cc55b)
- **API呼び出し**: $0
- **合計**: **$14/月**

### 完全自動モード
- **Mubert**: $14/月 → [**登録はこちら**](https://mubert.com/render/pricing?via=1cc55b)
- **API呼び出し**: $20〜$40/月
- **合計**: $34〜$54/月

> 💡 **Mubertアフィリエイトリンク経由で登録**すると、このプロジェクトの開発をサポートできます！

---

## 📋 21種類のテンプレート

<details>
<summary>🔊 <b>ノイズ系（3種）</b> - 集中力・睡眠導入</summary>

- **ピンクノイズ** - 最も人気、柔らかい音質
- **ホワイトノイズ** - 赤ちゃんの寝かしつけに最適
- **ブラウンノイズ** - 深い集中・低音好きに

</details>

<details>
<summary>🌿 <b>自然音（6種）</b> - リラックス・癒し</summary>

- **雨音** - 窓辺の優しい雨
- **水音** - 小川のせせらぎ
- **森** - 鳥のさえずり・風
- **海辺** - 波音・遠い海鳥
- **森の夜** - コオロギ・フクロウ
- **自然（汎用）** - 複合自然音

</details>

<details>
<summary>🔥 <b>焚き火系（2種）</b> - 温もり・安らぎ</summary>

- **炎** - 暖炉のパチパチ音
- **雨焚火** - テントで聞く雨＋焚き火

</details>

<details>
<summary>🎹 <b>ピアノ・音楽系（4種）</b> - 優しいメロディ</summary>

- **ピアノ** - 静かな夜想曲
- **自然ピアノ** - ピアノ＋森のせせらぎ
- **子守歌** - 赤ちゃん向けララバイ
- **雨窓ローファイ** - Lo-fi＋雨音

</details>

<details>
<summary>🌌 <b>アンビエント（3種）</b> - 深い瞑想</summary>

- **アンビエント** - シンセパッド・ドローン
- **星空ドローン** - 宇宙系サウンド
- **シータ波** - バイノーラルビート

</details>

<details>
<summary>✨ <b>特殊・ユニーク（3種）</b> - 独特な癒し</summary>

- **風鈴せせらぎ** - 和風BGM
- **ASMRソフトタッチ** - タッピング・ブラッシング
- **ささやきガイド** - 睡眠誘導ボイス付き

</details>

> 📝 すべてのテンプレートに **60 BPM指定Mubertプロンプト**・**推奨タイトル**・**タグ候補**・**カラーパレット**が含まれています

---

## 🎯 収益化ロードマップ

| 期間 | 目標 | 収益 |
|------|------|------|
| **2ヶ月目** | 登録者1,000人<br>再生時間4,000時間 | YouTube収益化達成 🎉 |
| **6ヶ月目** | 登録者10,000人<br>月間50万再生 | **月$500+** 💰 |
| **12ヶ月目** | 登録者50,000人<br>月間200万再生 | **月$3,000+** 🚀 |

**実績例**：
- 週5本投稿（ロング3本＋ショート2本）
- 平均再生時間: 30分
- RPM: $3〜$5

詳細戦略: [docs/戦略.md](docs/戦略.md)

---

## 📖 ドキュメント

| ドキュメント | 内容 | 対象 |
|------------|------|------|
| [QUICKSTART.md](automation/QUICKSTART.md) | 5分で始めるガイド | 初心者向け |
| [使い方.txt](automation/使い方.txt) | 重要事項・トラブル対処 | 全員必読 |
| [戦略.md](docs/戦略.md) | 収益化戦略・KPI・スケジュール | 本気で稼ぎたい人 |
| [今すぐ始める.txt](今すぐ始める.txt) | 最短3ステップガイド | とにかく急ぐ人 |

---

## 🛠️ 技術スタック

| カテゴリ | 技術 | 用途 |
|---------|------|------|
| **言語** | Python 3.10+ | メイン言語 |
| **GUI** | Tkinter | 操作画面 |
| **動画処理** | MoviePy | 動画生成・編集 |
| **音声処理** | Pydub | フェード・結合 |
| **API** | Google API Client | YouTube投稿 |
| **音源** | Mubert | 音楽生成（手動） |

---

## ❓ FAQ

<details>
<summary><b>Q: Mubert APIは使いますか？</b></summary>

**A: いいえ、使いません**（半自動モード）

- Mubertサイトで手動生成（Creator/Proプランの範囲内）
- API呼び出し費用: **$0**
- 月額$14のみで運用可能

</details>

<details>
<summary><b>Q: 1動画の制作時間は？</b></summary>

**A: 約60〜90分**

- Mubert音源生成: 5〜10分（手動）
- 動画生成: 20〜30分
- YouTubeアップロード: 30〜50分

放置可能なので実作業は10分程度

</details>

<details>
<summary><b>Q: 完全自動モードとの違いは？</b></summary>

| 項目 | 半自動 | 完全自動 |
|------|--------|---------|
| **費用** | $14/月 | $34〜$54/月 |
| **音源** | 手動生成 | API自動 |
| **時間** | 60〜90分 | 90〜200分 |
| **品質** | 選別可能 ⭐ | ランダム |

**推奨**: まず半自動で始める

</details>

<details>
<summary><b>Q: プログラミング知識は必要？</b></summary>

**A: 不要です**

- GUIで完結
- バッチファイルをダブルクリックするだけ
- コード編集不要

</details>

<details>
<summary><b>Q: Mac/Linuxでも使える？</b></summary>

**A: はい、使えます**

- Pythonスクリプトはクロスプラットフォーム
- バッチファイル(.bat)をシェルスクリプト(.sh)に変更
- 主要機能は全環境で動作

</details>

---

## ⚠️ 重要な注意事項

### 💰 費用・ライセンス
- **音源**: Mubert Creator/Pro（[登録](https://mubert.com/render/pricing?via=1cc55b)）商用利用許諾済み
- **コード**: MIT License（自由に改変・商用利用OK）
- **YouTube**: Content ID申請に対応（ライセンス証明保存推奨）

### 🔒 プライバシー
- `.gitignore`で認証情報を除外済み
- `credentials.json`・`.env`は含まれません
- 安全にPublic公開可能

---

## 🤝 コントリビューション

貢献を歓迎します！

- 🐛 バグ報告：[Issues](https://github.com/suyako-teck/sleep-bgm-automation/issues)
- 💡 機能提案：[Issues](https://github.com/suyako-teck/sleep-bgm-automation/issues)
- 🔧 Pull Request：[PRs](https://github.com/suyako-teck/sleep-bgm-automation/pulls)
- ⭐ Star：励みになります！

### 貢献例
- 新しいテンプレート追加
- 他言語対応
- Mac/Linux対応改善
- ドキュメント翻訳

---

## 📜 ライセンス

**MIT License** - 自由に使用・改変・商用利用OK

詳細: [LICENSE](LICENSE)

---

## 🔗 必要なサービス

### Mubert（音源生成）
[**→ Mubert Creator/Proプラン登録**](https://mubert.com/render/pricing?via=1cc55b) 

- Creator: $14/月
- Proプラン: $29/月
- 商用利用許諾済み

> 💝 上記アフィリエイトリンクからの登録で、このプロジェクトの継続開発をサポートできます（30%還元）

### Google Cloud Platform（YouTube API）
- YouTube Data API v3
- 無料（通常利用範囲内）

---

## 🙏 謝辞

- [Mubert](https://mubert.com/render/pricing?via=1cc55b) - AI音楽生成
- [MoviePy](https://zulko.github.io/moviepy/) - 動画処理
- [Pydub](https://github.com/jiaaro/pydub) - 音声処理

---

**⭐ Star & サポート**

このプロジェクトが役立ったら：
- ⭐ GitHubでStarしてください
- 🔗 [Mubertアフィリエイトリンク](https://mubert.com/render/pricing?via=1cc55b)から登録
- 📢 SNSでシェア

**開発者**: [@suyako-teck](https://github.com/suyako-teck)

