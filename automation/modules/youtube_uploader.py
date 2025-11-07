#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""YouTubeアップロードモジュール"""

import os
import logging
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

logger = logging.getLogger(__name__)
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']


class YouTubeUploader:
    """YouTubeアップロードクラス"""
    
    def __init__(self, credentials_file='credentials.json', token_file='token.json'):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.youtube = None
        
    def _get_authenticated_service(self):
        """認証"""
        creds = None
        
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=8080)
            
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        return build('youtube', 'v3', credentials=creds)
    
    def upload_video(self, video_path, title, description, tags, category=10, privacy='public', publish_at=None):
        """動画をアップロード"""
        logger.info("📤 YouTubeアップロード中...")
        
        if not self.youtube:
            self.youtube = self._get_authenticated_service()
        
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': str(category)
            },
            'status': {
                'privacyStatus': privacy,
                'selfDeclaredMadeForKids': False
            }
        }
        
        if publish_at:
            body['status']['publishAt'] = publish_at
            body['status']['privacyStatus'] = 'private'
        
        media = MediaFileUpload(video_path, chunksize=10*1024*1024, resumable=True)
        request = self.youtube.videos().insert(part=','.join(body.keys()), body=body, media_body=media)
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                logger.info(f"  進捗: {int(status.progress() * 100)}%")
        
        logger.info(f"✓ アップロード完了: {response['id']}")
        return response['id']

