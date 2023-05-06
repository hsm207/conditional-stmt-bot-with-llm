import json

import openai
import tenacity


@tenacity.retry(
    stop=tenacity.stop_after_attempt(3),
    wait=tenacity.wait_exponential(multiplier=1, min=1, max=60),
    retry=tenacity.retry_if_exception_type(openai.OpenAIError),
    reraise=True,
)
def _generate_completion(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    completed_text = response.choices[0].message["content"]
    return completed_text


def parse_device_instruction(message):
    prompt = f"""
    You are a syntax parser for a home automation system. Given a user's sentence like:
    
    if <condition> then <action>
    
    perform the following:

    1. Extract <condition> and <action>. If no condition, set it to null.
    2. Rewrite the extracted <condition> and <action> so that any of the user's personal and possessive pronouns are replaced with "the user".
    3. Create a friendly and enthusiastic text message to respond to the user. Replace any possessive references to the user with the corresponding second
       person possessive pronoun. References to the home automation system are to be in the first person.
    

    Process this sentence using the above steps:

    {message}

    Return the result in this format:

    {{
     
      "condition": <the rewritten condition from step 2>
      "action": <the rewritten action from step 2>
      "acknowledgement": <the acknowledgement text from step 3>

    }}

    """

    completion = _generate_completion(prompt)

    return json.loads(completion)
