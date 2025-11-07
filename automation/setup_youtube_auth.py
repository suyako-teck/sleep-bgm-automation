#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""YouTube API OAuth2認証セットアップ"""

from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import os

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']


def setup_auth():
    print("=" * 60)
    print("YouTube API認証")
    print("=" * 60)
    
    if not os.path.exists('credentials.json'):
        print("\n❌ credentials.json が見つかりません")
        print("\nGoogle Cloud Consoleから取得してください")
        return
    
    print("\n✓ credentials.json 検出")
    print("\nブラウザで認証...")
    
    try:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=8080)
        
        with open('token.json', 'wb') as token:
            pickle.dump(creds, token)
        
        print("\n✅ 認証成功！")
        print(f"✓ token.json 保存完了")
        
    except Exception as e:
        print(f"\n❌ エラー: {e}")


if __name__ == "__main__":
    setup_auth()

