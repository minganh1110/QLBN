from transformers import pipeline

unmasker = pipeline('fill-mask', model='distilbert-base-uncased')

result = unmasker("Hello I'm a [MASK] model.")

print(result)
