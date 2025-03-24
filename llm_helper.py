from langchain_groq.chat_models import ChatGroq
import os 

llm = ChatGroq(
    groq_api_key = os.environ.get('GROQ_API_KEY'),
    model = "llama-3.3-70b-versatile",
)

if __name__ == "__main__":
    response = llm.invoke("What are the two main ingredients in a chocolate cake?")
    print(response.content)