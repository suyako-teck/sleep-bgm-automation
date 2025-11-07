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

# 2. システムテスト（推奨）
test.bat

# 3. YouTube認証
auth.bat

# 4. ツール起動
manual.bat
```

### 🧪 テスト・診断ツール

| ツール | 用途 | 所要時間 |
|--------|------|---------|
| **test.bat** | 総合動作確認 | 30秒 |
| **benchmark.bat** | パフォーマンス測定 | 1分 |
| **test_amd_gpu.bat** | AMD GPU確認（RX 6750 XT用） | 10秒 |
| **debug.bat** | トラブル診断 | 30秒 |
| **reinstall.bat** | 再インストール | 2分 |

詳細: [START_HERE.txt](START_HERE.txt)、[docs/QUICKSTART.md](docs/QUICKSTART.md)

---

## 📁 フォルダ構成

```
automation/
│
├─【⭐ 実行ファイル】ダブルクリックで使う
│  ├─ manual.bat              動画作成GUI起動
│  ├─ setup.bat               初回セットアップ
│  ├─ test.bat                総合テスト
│  ├─ auth.bat                YouTube認証
│  ├─ benchmark.bat           性能測定
│  └─ reinstall.bat           再インストール
│
├─【プログラム本体】
│  ├─ manual_mode_v2.py       GUIアプリケーション
│  ├─ template_manager.py     テンプレート管理
│  └─ modules/                処理モジュール
│     ├─ audio_processor.py   音声編集
│     ├─ video_creator.py     動画生成
│     ├─ youtube_uploader.py  アップロード
│     └─ metadata_generator.py メタデータ
│
├─【ドキュメント】
│  └─ docs/
│     ├─ QUICKSTART.md           5分で始めるガイド
│     ├─ TROUBLESHOOTING.md      トラブル対処法
│     ├─ PERFORMANCE.md          高速化ガイド
│     ├─ AMD_GPU_SETUP.md        AMD GPU設定
│     └─ 使い方.txt              重要事項
│
├─【テスト・診断ツール】
│  └─ tests/
│     ├─ auto_test.py            総合テスト
│     ├─ benchmark.py            ベンチマーク
│     ├─ test_amd_gpu.bat        AMD GPU確認
│     ├─ debug.bat               デバッグ情報
│     └─ check_global_python.bat 環境チェック
│
└─【出力・設定】
   ├─ output/                生成された動画
   ├─ backgrounds/           背景画像
   ├─ requirements.txt       依存関係
   ├─ credentials.json       YouTube API
   └─ token.json             認証トークン
```

---

**推奨**: まずは半自動モード（manual.bat）から始めてください！

