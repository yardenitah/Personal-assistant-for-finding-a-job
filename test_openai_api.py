import openai

def test_openai_api(api_key):
    openai.api_key = api_key

    job_description = """
    SailPoint Data Access Security empowers organizations to discover, govern, and secure critical unstructured data and protect it from critical security risks. Designed as an integrated SaaS solution with Identity Security Cloud, it delivers enhanced intelligence on critical data to empower organizations to holistically improve data security posture, reduce risk, and streamline compliance efforts from day one. Our highly accomplished team is having fun and building cutting-edge technology.
    """
    resume = "Resume content here..."
    user_description = "A third-year software engineering student with proficiency in algorithms and data structures, seeking an internship in complex algorithm development and creative problem-solving."

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Job Description: {job_description}"},
        {"role": "user", "content": f"Resume: {resume}"},
        {"role": "user", "content": f"User Description: {user_description}"},
        {"role": "user", "content": "Based on the job description, resume, and user description, determine if this job is suitable for the user. Provide a suitability score (0-100) and a brief explanation."}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )

        result = response['choices'][0]['message']['content'].strip()
        print(f"API Response: {result}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    api_key = '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'
    test_openai_api(api_key)
