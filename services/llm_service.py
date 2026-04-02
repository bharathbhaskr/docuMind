import os
from openai import OpenAI
from dotenv import load_dotenv

# Load the .env file so OPENAI_API_KEY is available
load_dotenv()

# Create the client - it automatically reads OPENAI_API_KEY from environment
client = OpenAI()

def ask_llm(question: str, context: str = "") -> dict:
    """
    Send a question to OpenAI and get an answer back.
    
    question: what the user is asking
    context:  relevant text from their document (empty for now, filled in Phase 4)
    """

    # Build the system prompt - this tells the AI how to behave
    if context:
        system_prompt = f"""You are a helpful document assistant.
Answer the user's question using ONLY the context provided below.
If the answer is not in the context, say "I couldn't find that in the document."

Context:
{context}"""
    else:
        system_prompt = "You are a helpful assistant for the DocuMind application."

    # Make the API call
    response = client.chat.completions.create(
        model="gpt-4o-mini",   # cheap and fast - perfect for learning
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": question}
        ],
        max_tokens=500,        # cap the response length
        temperature=0.2        # lower = more focused, less creative
    )

    # Pull out the answer from the response object
    answer = response.choices[0].message.content

    # Return the answer plus useful metadata
    return {
        "answer": answer,
        "model": response.model,
        "tokens_used": response.usage.total_tokens
    }