# stoneEXPthree

一個使用 Three.js 製作的 3D 爆炸效果演示，包含石頭模型和粒子特效系統。

## 功能介紹

- 3D 石頭模型顯示與爆炸效果模擬
- 基於粒子系統的爆炸特效，產生隨機顏色和方向的爆炸粒子
- 支援透過 GUI 控制爆炸觸發、粒子大小和相機設定
- 可調整光源位置以改變場景照明效果
- 支援通過 URL 參數控制顯示模式和狀態檢查

## 技術實現

- 使用 Three.js 進行 3D 渲染
- 使用 OBJLoader 和 MTLLoader 加載 3D 模型和材質
- 實現 dat.GUI 控制界面
- 粒子系統模擬爆炸效果
- 支援狀態檢查 API 連接

## 使用方法

1. 開啟 `index.html` 檔案
2. 點擊界面上的 "explosionTrigger" 按鈕觸發爆炸效果
3. 通過 GUI 控制面板調整光源位置、粒子大小和相機參數

## URL 參數

可以通過 URL hash 參數控制程式行為：
- `clean=true` - 啟用簡潔模式，隱藏統計和控制面板
- `listenURL=url` - 設置狀態檢查的 URL

### listenURL 參數說明

`listenURL` 參數用於指定一個遠端 API 端點，程式會定期向該端點發送 HTTP 請求來檢查是否應該觸發爆炸效果。

- 格式：`listenURL=伺服器位址:埠號`（不需要包含協議前綴，程式會自動添加 `http://`）
- 預期回應：該端點應回傳純文字內容
  - 當回應內容為字串 `True` 時，程式會自動觸發爆炸效果
  - 其他回應內容則不會觸發任何動作
- 使用範例：`index.html#listenURL=192.168.1.100:8080`

此功能可用於遠端控制爆炸效果，適用於展示、互動裝置或透過其他應用程式觸發爆炸效果。

## 伺服器模組

在專案中包含了一個 TouchDesigner 網頁伺服器模組 (`serverFile.py`)，此模組作為示例，展示如何通過遠端 API 觸發爆炸效果。

### 伺服器功能

- 提供 HTTP API 端點來控制爆炸觸發狀態
- 支援 CORS，允許跨域請求
- 無需整合到主應用程式中，可獨立運行

### API 端點

- `/trigger` - 觸發爆炸效果 (設置觸發狀態為 True)
- `/UNtrigger` - 取消觸發 (設置觸發狀態為 False)
- `/status` - 返回當前觸發狀態 (True 或 False)

### 使用說明

此伺服器模組主要作為參考，適用於其他程式調用。當配合 `listenURL` 參數使用時，前端應用程式會定期檢查伺服器狀態並觸發相應的爆炸效果。

注意：此伺服器檔案包含在代碼庫中僅作為參考，幫助開發者理解如何實現遠端控制功能。

## 資源檔案

- `smoke.png` - 爆炸粒子使用的材質
- `Rock1/` - 包含石頭模型的 3D 資源檔案

## 開發環境

- Three.js v109
- Stats.js r16
- dat.GUI v0.7.3