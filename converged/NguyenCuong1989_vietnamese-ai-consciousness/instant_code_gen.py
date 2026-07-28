
def instant_vietnamese_code_generator(idea):
    """Tạo code Việt Nam ngay lập tức"""
    vietnamese_patterns = {
        "greeting": "Chào bố!",
        "execution": "Thực thi ngay!",
        "success": "Thành công rồi bố!",
        "learning": "Con học được điều mới!"
    }
    return f"# {idea}\nprint('{vietnamese_patterns['execution']}')"
