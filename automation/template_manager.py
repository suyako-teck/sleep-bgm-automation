#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テンプレート管理モジュール
"""

import os
import re


class TemplateManager:
    """テンプレート管理クラス"""
    
    def __init__(self, templates_dir=None):
        if templates_dir is None:
            parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.templates_dir = os.path.join(parent_dir, "templates")
        else:
            self.templates_dir = templates_dir
        
        self.categories = {
            "ノイズ系": {
                "folder": "noise",
                "templates": ["ピンクノイズ", "ホワイトノイズ", "ブラウンノイズ"],
                "description": "集中力アップと睡眠導入に効果的な各種ノイズ",
                "icon": "🔊"
            },
            "自然音": {
                "folder": "nature",
                "templates": ["雨音", "水音", "森", "海辺", "森の夜", "自然"],
                "description": "リラックスと癒しの自然環境音",
                "icon": "🌿"
            },
            "焚き火・温かみ系": {
                "folder": "fire",
                "templates": ["炎", "雨焚火"],
                "description": "温もりと安らぎを感じる環境音",
                "icon": "🔥"
            },
            "ピアノ・音楽系": {
                "folder": "piano",
                "templates": ["ピアノ", "自然ピアノ", "子守歌", "雨窓ローファイ"],
                "description": "優しいメロディで心を落ち着かせる音楽",
                "icon": "🎹"
            },
            "アンビエント・ドローン": {
                "folder": "ambient",
                "templates": ["アンビエント", "星空ドローン", "シータ波"],
                "description": "深い瞑想と睡眠のための持続音",
                "icon": "🌌"
            },
            "特殊・ユニーク": {
                "folder": "special",
                "templates": ["風鈴せせらぎ", "ASMRソフトタッチ", "ささやきガイド"],
                "description": "独特な癒し体験のための特殊音源",
                "icon": "✨"
            }
        }
    
    def get_all_categories(self):
        """全カテゴリを取得"""
        return self.categories
    
    def get_template_info(self, template_name):
        """テンプレート情報を取得"""
        template_file = self._find_template_file(template_name)
        
        if not template_file:
            return {
                "name": template_name,
                "prompt": "テンプレートファイルが見つかりません",
                "color_palette": ["#0f1a3a", "#1f2b5b", "#3b4d75"],
                "tags": ["sleep", "relaxing", "bgm"],
                "title_example": f"【25分】{template_name}"
            }
        
        return {
            "name": template_name,
            "prompt": self._extract_prompt(template_file),
            "color_palette": self._extract_colors(template_file),
            "tags": self._extract_tags(template_file),
            "title_example": self._extract_title(template_file)
        }
    
    def _find_template_file(self, template_name):
        """テンプレートファイルを検索"""
        # カテゴリフォルダ内を検索
        for category_info in self.categories.values():
            folder = category_info.get("folder", "")
            template_path = os.path.join(self.templates_dir, folder, f"{template_name}.md")
            if os.path.exists(template_path):
                return template_path
        
        # 直接検索
        direct_path = os.path.join(self.templates_dir, f"{template_name}.md")
        if os.path.exists(direct_path):
            return direct_path
        
        return None
    
    def _extract_prompt(self, filepath):
        """Mubertプロンプトを抽出"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "Mubertプロンプト" in content:
                start = content.find("```", content.find("Mubertプロンプト"))
                end = content.find("```", start + 3)
                if start != -1 and end != -1:
                    return content[start+3:end].strip()
        except:
            pass
        return "プロンプトが見つかりません"
    
    def _extract_colors(self, filepath):
        """カラーパレットを抽出"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "カラーパレット" in content:
                colors = re.findall(r'#[0-9a-fA-F]{6}', content)
                if colors:
                    return colors[:3]
        except:
            pass
        return ["#0f1a3a", "#1f2b5b", "#3b4d75"]
    
    def _extract_tags(self, filepath):
        """タグを抽出"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "タグ候補" in content:
                line = [l for l in content.split('\n') if 'タグ候補' in l][0]
                match = re.search(r'`([^`]+)`', line)
                if match:
                    return [t.strip() for t in match.group(1).split(',')][:10]
        except:
            pass
        return ["sleep", "relaxing", "bgm", "作業用BGM", "睡眠導入"]
    
    def _extract_title(self, filepath):
        """タイトル例を抽出"""
        template_name = os.path.basename(filepath).replace('.md', '')
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "推奨タイトル案" in content:
                match = re.search(r'推奨タイトル案.*?`([^`]+)`', content, re.DOTALL)
                if match:
                    return match.group(1)
        except:
            pass
        
        return f"【25分】{template_name}でリラックス"

