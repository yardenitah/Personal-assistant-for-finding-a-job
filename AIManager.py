import openai

class AIManager:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def evaluate_job_suitability(self, job_description, resume, user_description):
        prompt = f"""
        Job Description: {job_description}
        Resume: {resume}
        User Description: {user_description}

        Based on the job description, resume, and user description, determine if this job is suitable for the user. Provide a suitability score (0-100) and a brief explanation.
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7,
            top_p=1,
            n=1,
            stop=None
        )

        result = response['choices'][0]['message']['content'].strip()
        return result
