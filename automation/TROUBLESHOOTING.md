# 🔧 トラブルシューティングガイド

## ❌ エラー: モジュールがインストールされていません

### 症状

```
❌ 致命的な問題が見つかりました:
  • PILがインストールされていません
  • google.oauth2がインストールされていません
  • googleapiclientがインストールされていません
  • yamlがインストールされていません
```

### 原因

仮想環境が正しく有効化されていない、または依存関係がインストールされていません。

---

## 🔧 解決方法

### 方法1: 再インストール（推奨）

```bash
cd C:\Users\suyako\Desktop\sleep\automation
reinstall.bat
```

このスクリプトが：
1. 仮想環境を有効化
2. pipをアップグレード
3. 既存パッケージをクリーンアップ
4. requirements.txtから再インストール

---

### 方法2: 手動で確認

#### ステップ1: 仮想環境を有効化

```bash
cd C:\Users\suyako\Desktop\sleep
venv\Scripts\activate.bat
```

プロンプトが `(venv)` で始まることを確認：

```
(venv) C:\Users\suyako\Desktop\sleep>
```

#### ステップ2: インストール状況を確認

```bash
pip list
```

以下が表示されるはず：
```
Package                      Version
---------------------------- -------
Pillow                       10.x.x
pydub                        0.25.x
moviepy                      1.0.3
google-api-python-client     2.x.x
google-auth-oauthlib         1.x.x
pyyaml                       6.x.x
...
```

#### ステップ3: 不足しているパッケージをインストール

```bash
cd automation
pip install -r requirements.txt
```

---

### 方法3: 仮想環境を再作成

#### ステップ1: 古い仮想環境を削除

```bash
cd C:\Users\suyako\Desktop\sleep
rmdir /s /q venv
```

#### ステップ2: 再セットアップ

```bash
cd automation
setup.bat
```

---

## 🔍 確認方法

### 正常に動作しているか確認

```bash
cd C:\Users\suyako\Desktop\sleep
venv\Scripts\activate.bat
python -c "import pydub, moviepy, PIL, yaml; print('✅ すべてのモジュールが正常')"
```

成功すると：
```
✅ すべてのモジュールが正常
```

---

## 🚨 よくあるエラーと解決策

### エラー1: `venv\Scripts\activate.bat` が見つからない

**原因:** 仮想環境が作成されていない

**解決策:**
```bash
cd C:\Users\suyako\Desktop\sleep
python -m venv venv
cd automation
setup.bat
```

---

### エラー2: `pip install` がエラーになる

**原因:** pipのバージョンが古い

**解決策:**
```bash
venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r automation\requirements.txt
```

---

### エラー3: `moviepy` のインストールでエラー

**原因:** 依存関係の問題

**解決策:**
```bash
venv\Scripts\activate.bat
pip install imageio==2.31.1
pip install imageio-ffmpeg>=0.4.9
pip install moviepy==1.0.3
```

---

### エラー4: 仮想環境が有効化されない

**症状:**
```
⚠️  グローバルPythonで実行中
   manual.bat から起動してください
```

**原因:** 直接Pythonスクリプトを実行している

**解決策:**
```bash
# ❌ 間違い
python manual_mode_v2.py

# ✅ 正しい
manual.bat
```

---

## 📋 チェックリスト

起動前に以下を確認：

- [ ] Pythonがインストールされている（`python --version`）
- [ ] 仮想環境が存在する（`sleep\venv\` フォルダ）
- [ ] requirements.txtが存在する（`automation\requirements.txt`）
- [ ] manual.batから起動している（直接Pythonスクリプトを実行しない）

---

## 🆘 それでも解決しない場合

### デバッグ情報を収集

```bash
cd C:\Users\suyako\Desktop\sleep\automation
debug.bat > debug_log.txt
```

debug_log.txtの内容を確認してください。

---

## 📞 サポート

GitHub Issues:
https://github.com/suyako-teck/sleep-bgm-automation/issues

