

# Example code to use GPT-Neo with transformers
from transformers import GPTNeoForCausalLM, GPT2Tokenizer

# Load the model and tokenizer
model = GPTNeoForCausalLM.from_pretrained('EleutherAI/gpt-neo-1.3B')
tokenizer = GPT2Tokenizer.from_pretrained('EleutherAI/gpt-neo-1.3B')

# Generate text
prompt = "Once upon a time"
#inputs = tokenizer(prompt, return_tensors="pt")
input_ids = tokenizer.encode("Your input text", return_tensors="pt")
attention_mask = (input_ids != tokenizer.pad_token_id).long()

output = model.generate(input_ids=input_ids, attention_mask=attention_mask)

#outputs = model.generate(inputs.input_ids, max_length=100)

print(tokenizer.decode(outputs[0], skip_special_tokens=True))
