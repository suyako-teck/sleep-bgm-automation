# GitHubアップロード手順

## ステップ1: GitHubでリポジトリ作成

1. https://github.com/ にアクセス
2. 右上の「+」→「New repository」
3. 以下を入力：
   - **Repository name**: `sleep-bgm-automation`
   - **Description**: `AI Music BGM Auto-Generator for YouTube - 睡眠・作業用BGM自動生成ツール`
   - **Public** または **Private** を選択
   - **Add README**: チェックしない（既に作成済み）
   - **Add .gitignore**: チェックしない（既に作成済み）
   - **Choose a license**: チェックしない（MIT Licenseを追加済み）

4. 「Create repository」をクリック

---

## ステップ2: ローカルリポジトリをプッシュ

GitHubに表示される指示に従います：

```bash
cd C:\Users\suyako\Desktop\sleep

# リモートリポジトリを追加
git remote add origin https://github.com/YOUR_USERNAME/sleep-bgm-automation.git

# ブランチ名をmainに変更（推奨）
git branch -M main

# プッシュ
git push -u origin main
```

**YOUR_USERNAME** の部分を自分のGitHubユーザー名に置き換えてください。

---

## ステップ3: README_GITHUB.mdをREADME.mdに

GitHubで表示されるREADMEを英語版にする場合：

```bash
# 現在のREADME.mdをバックアップ
mv README.md README_JP.md

# 英語版をREADME.mdに
mv README_GITHUB.md README.md

# コミット＆プッシュ
git add .
git commit -m "Update README for GitHub"
git push
```

---

## オプション: GitHub Actionsで自動化

将来的にGitHub Actionsでスケジュール投稿も可能です。

---

## 完了後

リポジトリURL:
https://github.com/YOUR_USERNAME/sleep-bgm-automation

このURLを:
- YouTubeチャンネル概要欄に記載
- SNSでシェア
- ポートフォリオに追加

---

**注意**: 
- `credentials.json` や `.env` は.gitignoreで除外済み
- 個人情報は含まれません
- 安全にPublicで公開できます

