import os
from openai import AsyncOpenAI
from database import search_culture_db

client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

async def generate_response(user_message: str):
    # 1. Create an embedding for the user's message
    emb_response = await client.embeddings.create(
        input=user_message,
        model="text-embedding-3-small"
    )
    query_vector = emb_response.data[0].embedding

    # 2. Search database using that vector
    context_results = await search_culture_db(query_vector)
    
    # 3. Format the context for the AI
    context_str = "\n\n".join(
        [f"Found Info: {r['title']} - {r['content']} (Media: {r['media_url']})" for r in context_results]
    )

    # 4. Ask the LLM to answer using the context
    system_prompt = (
        "You are a helpful assistant for cultural heritage. "
        "Answer the user's question in their own language (Khmer, Xhosa, or English). "
        "Use the provided context to answer if relevant."
    )

    response = await client.chat.completions.create(
        model="gpt-4o", # or "qwen-plus"
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context:\n{context_str}\n\nUser Question: {user_message}"}
        ]
    )
    return response.choices[0].message.content