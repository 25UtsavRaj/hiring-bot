from vertexai.preview.generative_models import GenerativeModel, Part # Changed import
import vertexai
import json

def generate_screening_questions(jd_text: str):
    try:
        # Initialize Vertex AI with your project and location
        vertexai.init(project="hackathon-martificial-minds", location="asia-east1")

        # Use a Gemini model for chat capabilities
        # Recommended: "gemini-1.5-flash-preview-0520" for speed/cost, or "gemini-1.5-pro-preview-0520" for more complex reasoning.
        model = GenerativeModel("gemini-1.5-flash-preview-0520") # Changed model initialization

        prompt = f"""
        You are an HR assistant AI. Based on the job description below, generate 4 to 6 simple screening questions
        to evaluate candidate eligibility. Use YES/NO or short factual responses only. Each question must be tagged with a unique field name.

        Return response in JSON format like:
        [
          {{ "question": "Do you have a postgraduate degree?", "field": "postgraduate" }},
          {{ "question": "Do you own a two-wheeler?", "field": "bike" }}
        ]

        Job Description:
        {jd_text}
        """

        # For GenerativeModel, you typically use generate_content.
        # If you need multi-turn conversation, you'd use model.start_chat() and then chat.send_message().
        response = model.generate_content(
            contents=[Part.from_text(prompt)],
            generation_config={"temperature": 0.2}
        )

        # Gemini's response.text contains the generated content
        return json.loads(response.text)

    except Exception as e:
        print("Error generating or parsing Gemini response:", e)
        # It's good practice to re-raise or handle specific errors more granularly
        # raise # Uncomment to re-raise the exception after printing
        return []