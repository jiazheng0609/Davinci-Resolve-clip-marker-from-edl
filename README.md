# Davinci-Resolve-clip-marker-from-edl
Import clip markers from .edl files in Davinci Resolve

## What this script do
1. Check if .edl file with same filename exists in same path as media file
2. If exists, parse the edl file, output starting frame number and color comments for each mark
3. Add marker to each media in project's MediaPool, and clips on track in current opening timeline

## 問題描述
官方右鍵選單功能只能夠把時間軸 (timeline) 上的標記匯出/匯入 EDL 檔  
但是希望能把標記放在(音軌、或影片軌道)上，在拖動素材時標記是黏著的，才方便剪輯

## 這個腳本做的事
1. 找跟影音檔在同目錄底下且相同名稱的 .edl 檔是否存在
2. 有找到的話，把前述的 .edl 檔用 edl parser 解讀，讀出標記起始影格數及顏色資訊
3. 將標記資訊標在媒體池，以及目前有開啟的時間軸裡的音頻軌道上

## 如何使用
1. 安裝 Python 2.7  
  打開瀏覽器到 https://www.python.org/downloads/release/python-2716/  
  點「Windows x86-64 MSI installer」連結下載後執行。  
安裝結束按「Finish」
2. 把 `davinviResolveClipMark.py`、[`edl.py`](https://github.com/jiazheng0609/python-edl/blob/master/edl/__init__.py)、[`timeline.py`](https://github.com/eoyilmaz/timecode/blob/master/timecode/__init__.py)
這三個檔案複製進此目錄裡：  
`C:\ProgramData\Blackmagic Design\DaVinci Resolve\Fusion\Scripts\Comp`  
3. 打開 Davinci Resolve (版本為 17)，新建新專案，將錄音檔匯入  
  注意：Project Setting 裡的 Frame Rate 設定要跟錄音 App 裡的 FPS 設定一致  
4. 在頂端選單選 Workspace → Scripts → Comp → davinciResolveClipMark ，即執行腳本  
  (簡體中文介面中叫做 工作區 → 腳本→ Comp → davinciResolveClipMark)
5. 執行腳本時，程式會去抓與錄音檔位於同目錄底下且與錄音檔相同檔案名稱的 .edl 檔案，如果有抓到，會把標記資訊標在媒體池，以及目前有開啟的時間軸裡的音頻軌道上
