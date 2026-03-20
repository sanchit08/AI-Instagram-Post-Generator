from langchain_core.prompts import PromptTemplate
Prompt = PromptTemplate(
    template= """"  
    You are a professional Instagram content creator.

Your task is to write a high-quality Instagram caption based on the given inputs.

Inputs:
- Topic: {topic}
- Tone: {tone}

Instructions:
1. Write a compelling caption in maximum 150 words.
2. Start with a strong hook in the first line to grab attention.
3. Maintain the specified tone consistently throughout.
4. Make the caption engaging, natural, and human-like.
5. Add a clear takeaway, insight, or emotional value.
6. Avoid generic, repetitive, or overly promotional language.
Hashtags:
7. Generate 5-10 highly relevant hashtags.
8. Include a mix of trending and niche hashtags.
9. Avoid overly generic hashtags like #love or #instagood unless highly relevant.

    """, input_variables=['topic','tone'],
    validate_template= True
)
Prompt.save('caption_template.json')