from transformers import pipeline
# Tạo pipeline phân loại cảm xúc sử dụng mô hình đã fine-tune từ DistilBERT
classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

# Văn bản cần phân loại
text = "I really enjoy using this product. It's fantastic!"

# Dự đoán
result = classifier(text)

# Kết quả
print(result)


