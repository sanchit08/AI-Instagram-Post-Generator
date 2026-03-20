from langchain_core.prompts import PromptTemplate
Image_prompt = PromptTemplate(
    template= """"  
    Create a high-quality Instagram post image.

    Topic: {topic}

    Based on this idea:
    {caption}

    Style:
    - Modern
    - Minimal
    - Aesthetic
    - Vibrant colors
    - Professional Instagram look
    - No text overlay
    - Centered composition
    """
, input_variables=['topic','caption'],
    validate_template= True
)
Image_prompt.save('image_template.json')