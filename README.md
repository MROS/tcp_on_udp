# 網路作業2 報告

---

## 系統需求
- python3

警告：僅在 linux 下以 python3.4.2 進行測試

## 執行

- 開啟 agent

```  bash
python3 agent.py drop_rate
```

-  開啟 receiver

```bash
python3 receiver.py filename
```

- 開啟 sender

```bash
python3 sender.py filename
```

## 程式細節

以 python pickle 來產生 python 物件的二進位代表，再傳送之。

## 困難

這次用 python 這種不熟的語言短時間邊學邊做，沒辦法寫出很優雅的程式碼。並且 python 的標準庫對於 unix 系統呼叫的包裝有所缺失，使用上並不方便，只能以較為狡詐的方式解決。

timer 的設置中無論是 python 標準庫或 unix 系統呼叫提供的機制都不夠漂亮，需要考慮的細節不少，算是實做上的最大困難。

另外，udp在極為壅塞的狀況下，在本機依然有掉包的可能性，推估是 udp 內部維護的 buffer 不大（預設128KB），當超出 buffer 大小，udp 將自動丟棄之。