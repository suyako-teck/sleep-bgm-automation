#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""メタデータ生成モジュール"""

class MetadataGenerator:
    """メタデータ生成クラス"""
    
    def generate_tags_from_template(self, template_name):
        """テンプレート名からタグを生成"""
        base_tags = ["sleep", "relaxing music", "bgm", "作業用BGM", "睡眠導入"]
        
        template_tags = {
            "ピンクノイズ": ["pink noise", "noise", "focus"],
            "ホワイトノイズ": ["white noise", "concentration"],
            "ブラウンノイズ": ["brown noise", "deep focus"],
            "雨音": ["rain sounds", "rain"],
            "ピアノ": ["piano", "peaceful piano"],
            "アンビエント": ["ambient", "drone", "meditation"],
            "自然": ["nature sounds", "forest"],
            "炎": ["fireplace", "campfire"],
            "海辺": ["ocean waves", "beach"]
        }
        
        additional = []
        for key, tags in template_tags.items():
            if key in template_name:
                additional.extend(tags)
                break
        
        return base_tags + additional

