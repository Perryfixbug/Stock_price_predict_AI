
# Invest AI - Hỗ trợ đầu tư

Dự án tạo trang web có tích hợp AI dự đoán giá cổ phiếu và chatbot hỗ trợ đầu tư




## Installation

Cài đặt và chạy venv

```bash
    pip -m venv myenv
    myenv/Scripts/activate
```
Tải các thư viện cần thiết
```bash
    pip install -r requirements.txt
```
    
## Appendix

Dự án có sử dụng API key của Alpha Vantage, NewsAPI

Tại file config.py
```base
    NEWS_API_KEY = "YOUR_API_KEY"
    ALPHA_VANTAGE_API_KEY_2 = "YOUR_API_KEY"
```

## Deployment

Chạy streamlit trong venv

```bash
  streamlit run Home.py
```

