#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
半自動モード v2 - テンプレート選択＋ショート対応
⚠️ Mubert APIは使用しません（費用節約）
"""

import os
import sys
import logging
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import webbrowser

# ログ設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# モジュールインポート
try:
    from modules.audio_processor import AudioProcessor
    from modules.video_creator import VideoCreator
    from modules.youtube_uploader import YouTubeUploader
    from modules.metadata_generator import MetadataGenerator
    from template_manager import TemplateManager
except ImportError as e:
    print(f"❌ モジュールのインポートエラー: {e}")
    print("setup.bat を実行してください")
    sys.exit(1)


class ManualModeGUI:
    """半自動モードGUI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("AI音楽BGM 半自動生成ツール v2 - API不使用")
        self.root.geometry("1400x850")
        
        self.checklist_vars = {}
        self.audio_files = []
        self.config = {}
        self.template_manager = TemplateManager()
        self.video_type = tk.StringVar(value="long")
        self.generated_long_video = None
        self.selected_template = None
        
        self.create_widgets()
    
    def create_widgets(self):
        """ウィジェット作成"""
        
        # 左：チェックリスト
        left_frame = ttk.Frame(self.root, padding="10", width=300)
        left_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.W))
        left_frame.grid_propagate(False)
        
        ttk.Label(left_frame, text="📋 制作チェックリスト", font=('Arial', 12, 'bold')).pack(pady=10)
        
        checklist_items = [
            ("step1", "1. テンプレート選択"),
            ("step2", "2. プロンプト確認"),
            ("step3", "3. Mubert音源生成"),
            ("step4", "4. 音源ファイル選択"),
            ("step5", "5. 形式選択"),
            ("step6", "6. 設定入力"),
            ("step7", "7. 動画生成"),
            ("step8", "8. アップロード")
        ]
        
        for key, text in checklist_items:
            var = tk.BooleanVar()
            self.checklist_vars[key] = var
            ttk.Checkbutton(left_frame, text=text, variable=var, command=self.update_progress).pack(anchor=tk.W, pady=3)
        
        self.progress_label = ttk.Label(left_frame, text="進捗: 0/8", font=('Arial', 11, 'bold'), foreground='blue')
        self.progress_label.pack(pady=15)
        
        next_frame = ttk.LabelFrame(left_frame, text="次のステップ", padding="10")
        next_frame.pack(fill=tk.X, pady=10)
        self.next_step_label = tk.Label(next_frame, text="テンプレート選択", wraplength=260, justify=tk.LEFT, fg='green')
        self.next_step_label.pack()
        
        # 中央：テンプレート選択
        center_frame = ttk.Frame(self.root, padding="10")
        center_frame.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.W, tk.E))
        
        ttk.Label(center_frame, text="🎵 テンプレート選択", font=('Arial', 12, 'bold')).pack(pady=10)
        
        self.category_notebook = ttk.Notebook(center_frame)
        self.category_notebook.pack(fill=tk.BOTH, expand=True)
        self.create_category_tabs()
        
        # プロンプト表示
        prompt_frame = ttk.LabelFrame(center_frame, text="📝 Mubertプロンプト（手動生成用）", padding="10")
        prompt_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        ttk.Label(prompt_frame, text="⚠️ API不使用 - Mubertサイトで手動生成", foreground='red', font=('Arial', 9, 'bold')).pack(pady=5)
        
        self.prompt_text = scrolledtext.ScrolledText(prompt_frame, height=5, wrap=tk.WORD)
        self.prompt_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        btn_frame = ttk.Frame(prompt_frame)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="📋 コピー", command=self.copy_prompt, width=15).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_frame, text="🌐 Mubert開く", command=self.open_mubert, width=15).pack(side=tk.LEFT, padx=3)
        
        # 右：設定・実行
        right_frame = ttk.Frame(self.root, padding="10")
        right_frame.grid(row=0, column=2, sticky=(tk.N, tk.S, tk.W, tk.E))
        
        # 形式選択
        format_frame = ttk.LabelFrame(right_frame, text="📹 動画形式", padding="10")
        format_frame.pack(fill=tk.X, pady=10)
        ttk.Radiobutton(format_frame, text="🎬 ロング（25分〜8時間）", variable=self.video_type, value="long").pack(anchor=tk.W)
        ttk.Radiobutton(format_frame, text="📱 ショート（60秒）", variable=self.video_type, value="short").pack(anchor=tk.W)
        
        # 音源選択
        audio_frame = ttk.LabelFrame(right_frame, text="🎵 音源（手動ダウンロード）", padding="10")
        audio_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(audio_frame, text="音源追加", command=self.add_audio).pack(pady=3, fill=tk.X)
        self.audio_listbox = tk.Listbox(audio_frame, height=4)
        self.audio_listbox.pack(fill=tk.X, pady=3)
        
        # 設定
        settings_frame = ttk.LabelFrame(right_frame, text="⚙️ 設定", padding="10")
        settings_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(settings_frame, text="タイトル:").grid(row=0, column=0, sticky=tk.W)
        self.title_entry = ttk.Entry(settings_frame, width=40)
        self.title_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=3)
        
        ttk.Label(settings_frame, text="長さ:").grid(row=1, column=0, sticky=tk.W)
        duration_frame = ttk.Frame(settings_frame)
        duration_frame.grid(row=1, column=1, sticky=tk.W, pady=3)
        
        self.duration_var = tk.StringVar(value="480")
        duration_options = [
            ("25分（ポモドーロ）", "25"),
            ("1時間（短時間作業）", "60"),
            ("3時間（作業セッション）", "180"),
            ("5時間（長時間作業）", "300"),
            ("8時間（睡眠）", "480"),
            ("10時間（深い睡眠）", "600"),
            ("12時間（超長時間）", "720")
        ]
        
        duration_combo = ttk.Combobox(duration_frame, textvariable=self.duration_var, width=25, state='readonly')
        duration_combo['values'] = [f"{label} - {mins}分" for label, mins in duration_options]
        duration_combo.set("8時間（睡眠） - 480分")
        duration_combo.pack(side=tk.LEFT)
        
        ttk.Label(duration_frame, text="※音源を自動ループ", foreground='gray', font=('Arial', 8)).pack(side=tk.LEFT, padx=5)
        
        settings_frame.columnconfigure(1, weight=1)
        
        # 実行ボタン
        button_frame = ttk.LabelFrame(right_frame, text="🚀 実行（API費用0円）", padding="10")
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(button_frame, text="✅ YouTube APIのみ使用（無料）", foreground='green', font=('Arial', 8)).pack(pady=5)
        
        ttk.Button(button_frame, text="🎬 動画生成", command=self.generate_video, width=25).pack(pady=3, fill=tk.X)
        ttk.Button(button_frame, text="📤 アップロード", command=self.upload_video, width=25).pack(pady=3, fill=tk.X)
        ttk.Button(button_frame, text="🚀 生成＋アップロード", command=self.generate_and_upload, width=25).pack(pady=3, fill=tk.X)
        
        # ログ
        log_frame = ttk.LabelFrame(self.root, text="📊 ログ", padding="5")
        log_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # ステータスバー
        self.status_var = tk.StringVar(value="準備完了")
        ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W).grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        self.root.columnconfigure(1, weight=2)
        self.root.columnconfigure(2, weight=2)
        self.root.rowconfigure(0, weight=1)
    
    def create_category_tabs(self):
        """カテゴリタブ作成"""
        for category, info in self.template_manager.get_all_categories().items():
            tab = ttk.Frame(self.category_notebook)
            self.category_notebook.add(tab, text=f"{info['icon']} {category}")
            
            ttk.Label(tab, text=info['description'], foreground='gray').pack(pady=10)
            
            btn_container = ttk.Frame(tab)
            btn_container.pack(fill=tk.BOTH, expand=True, padx=10)
            
            for i, template_name in enumerate(info['templates']):
                ttk.Button(btn_container, text=template_name, command=lambda t=template_name: self.select_template(t), width=20).grid(row=i//2, column=i%2, padx=5, pady=5)
    
    def select_template(self, template_name):
        """テンプレート選択"""
        self.selected_template = template_name
        self.log(f"✓ 選択: {template_name}")
        
        info = self.template_manager.get_template_info(template_name)
        
        self.prompt_text.delete(1.0, tk.END)
        self.prompt_text.insert(1.0, info['prompt'])
        
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, info['title_example'])
        
        self.config['tags'] = info['tags']
        
        self.checklist_vars['step1'].set(True)
        self.update_progress()
        self.status_var.set(f"{template_name} - Mubertで音源生成してください")
    
    def open_mubert(self):
        """Mubertサイトを開く"""
        webbrowser.open("https://mubert.com/render")
        self.log("🌐 Mubert開きました")
        messagebox.showinfo("手順", "1. プロンプトを貼り付け\n2. Duration: 600秒\n3. Generate\n4. Download\n5. 音源追加")
    
    def copy_prompt(self):
        """プロンプトコピー"""
        prompt = self.prompt_text.get(1.0, tk.END).strip()
        if not prompt or "見つかりません" in prompt:
            messagebox.showwarning("警告", "先にテンプレート選択")
            return
        
        self.root.clipboard_clear()
        self.root.clipboard_append(prompt)
        self.log("✓ コピー完了")
        
        if messagebox.askyesno("コピー完了", "Mubertサイトを開きますか？"):
            self.open_mubert()
        
        self.checklist_vars['step2'].set(True)
        self.update_progress()
    
    def add_audio(self):
        """音源追加"""
        files = filedialog.askopenfilenames(title="音源選択", filetypes=[("Audio", "*.mp3 *.wav"), ("All", "*.*")])
        for file in files:
            if file not in self.audio_files:
                self.audio_files.append(file)
                self.audio_listbox.insert(tk.END, os.path.basename(file))
        
        if files:
            self.checklist_vars['step3'].set(True)
            self.checklist_vars['step4'].set(True)
            self.update_progress()
            self.log(f"✓ {len(files)}個追加")
    
    def update_progress(self):
        """進捗更新"""
        completed = sum(1 for v in self.checklist_vars.values() if v.get())
        self.progress_label.config(text=f"進捗: {completed}/8")
    
    def log(self, msg):
        """ログ表示"""
        self.log_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def generate_video(self):
        """動画生成"""
        if not self.audio_files:
            messagebox.showerror("エラー", "音源を選択してください")
            return
        
        self.status_var.set("🎬 動画生成中...")
        self.log("=" * 50)
        self.log("動画生成開始")
        
        try:
            # 目標時間を取得（コンボボックスから分数を抽出）
            duration_text = self.duration_var.get()
            # "8時間（睡眠） - 480分" から "480" を抽出
            target_minutes = int(duration_text.split(" - ")[1].replace("分", ""))
            self.log(f"🎯 目標時間: {target_minutes}分")
            
            processor = AudioProcessor()
            
            # 音源を結合＋ループ処理
            final_audio = processor.process_audio(
                self.audio_files, 
                fade_in=3, 
                fade_out=5, 
                crossfade=1, 
                target_volume=-6, 
                output_name=f"{self.selected_template}_audio.mp3",
                target_duration_minutes=target_minutes
            )
            
            self.log("✓ 音声処理完了")
            
            creator = VideoCreator()
            
            is_short = self.video_type.get() == "short"
            resolution = (1080, 1920) if is_short else (1920, 1080)
            output_name = f"{'short' if is_short else 'long'}_{self.selected_template}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
            
            video_path = creator.create_video(final_audio, None, resolution, 30, self.title_entry.get(), "", output_name)
            
            self.config['video_path'] = video_path
            self.generated_long_video = video_path
            
            self.log(f"✓ 動画完成: {os.path.basename(video_path)}")
            self.status_var.set("✅ 動画生成完了")
            
            self.checklist_vars['step7'].set(True)
            self.update_progress()
            
            if messagebox.askyesno("完了", f"動画生成完了\n\nフォルダを開きますか？"):
                os.startfile(os.path.dirname(os.path.abspath(video_path)))
            
        except Exception as e:
            self.log(f"❌ エラー: {e}")
            self.status_var.set("❌ エラー")
            messagebox.showerror("エラー", str(e))
    
    def upload_video(self):
        """アップロード"""
        if 'video_path' not in self.config:
            file = filedialog.askopenfilename(title="動画選択", filetypes=[("Video", "*.mp4"), ("All", "*.*")])
            if not file:
                return
            self.config['video_path'] = file
        
        self.status_var.set("📤 アップロード中...")
        self.log("=" * 50)
        self.log("アップロード開始")
        
        try:
            uploader = YouTubeUploader()
            metadata_gen = MetadataGenerator()
            
            tags = self.config.get('tags', metadata_gen.generate_tags_from_template(self.selected_template or ""))
            
            description = f"""ご視聴ありがとうございます。
{self.duration_entry.get()}分間の{self.selected_template or 'BGM'}です。

▷ 特徴
- 60 BPMの落ち着いたサウンド
- 長時間再生対応

▷ 制作
- 音源：Mubert (Creator/Proプラン)
- 制作日：{datetime.now().strftime("%Y-%m-%d")}

#sleep #relaxing #bgm #作業用BGM #睡眠導入
"""
            
            video_id = uploader.upload_video(self.config['video_path'], self.title_entry.get(), description, tags[:15], 10, 'public')
            
            url = f"https://www.youtube.com/watch?v={video_id}"
            self.log(f"✅ アップロード完了")
            self.log(f"🔗 {url}")
            
            self.root.clipboard_clear()
            self.root.clipboard_append(url)
            
            self.status_var.set("✅ 完了")
            self.checklist_vars['step8'].set(True)
            self.update_progress()
            
            messagebox.showinfo("完了", f"アップロード完了！\n\n{url}\n\nURLコピー済み")
            
        except Exception as e:
            self.log(f"❌ エラー: {e}")
            self.status_var.set("❌ エラー")
            messagebox.showerror("エラー", str(e))
    
    def generate_and_upload(self):
        """生成＋アップロード"""
        self.checklist_vars['step6'].set(True)
        self.update_progress()
        
        self.generate_video()
        
        if 'video_path' in self.config and os.path.exists(self.config['video_path']):
            if messagebox.askyesno("確認", "YouTubeにアップロードしますか？"):
                self.upload_video()


def main():
    root = tk.Tk()
    app = ManualModeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

