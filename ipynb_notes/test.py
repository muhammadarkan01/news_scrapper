from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Konfigurasi Ollama
ollama_model = Ollama(model="aya")  # Ganti dengan model Ollama yang sesuai

# Membuat template prompt
prompt_template = "Halo, bagaimana kabarmu hari ini?"

# Membuat chain dengan model Ollama
llm_chain = LLMChain(llm=ollama_model, prompt=prompt_template)

# Menjalankan dan mendapatkan respons
response = llm_chain.run()

# Menampilkan hasil
print("Response:", response)
