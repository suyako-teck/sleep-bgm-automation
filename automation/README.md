# AI音楽BGM自動生成・アップロードツール

Mubert音源から動画を作成してYouTubeへアップロードする自動化ツールです。

---

## 🎨 半自動モード（推奨）⭐

**API不使用・月$14のみ**

### 起動方法
```bash
manual.bat
```

### 特徴
- ✅ Mubert APIを使わない（費用節約）
- ✅ GUIで簡単操作
- ✅ カテゴリ別テンプレート選択
- ✅ プロンプト自動表示＋コピー
- ✅ Mubertサイトへワンクリック
- ✅ ロング/ショート両対応
- ✅ チェックリストで進捗管理

### 使用するAPI
- YouTube Data API のみ（無料）
- Mubert API は使用しません

### 月額費用
- Mubert Creator/Pro: $14
- API呼び出し: $0
- **合計: $14/月**

詳細: [MANUAL_MODE.md](MANUAL_MODE.md)

---

## 🤖 完全自動モード

**すべて自動・月$34〜$54**

### 起動方法
```bash
run.bat configs\ピンクノイズ_8時間.yaml
```

### 特徴
- ✅ Mubert APIで音源自動生成
- ✅ 完全放置でOK
- ✅ スケジュール投稿対応

### 月額費用
- Mubert: $14
- API呼び出し: $20〜$40
- **合計: $34〜$54/月**

---

## 🚀 初回セットアップ

```bash
# 1. セットアップ実行
setup.bat

# 2. YouTube認証
auth.bat

# 3. ツール起動
manual.bat
```

詳細: [QUICKSTART.md](QUICKSTART.md)

---

**推奨**: まずは半自動モード（manual.bat）から始めてください！

