import ollama 
import json

def ochat(model, prompt: str, history: list, save_prompt='user', 
          save_response='assistant', format='', options=None, system=''
          ) -> dict | str:
    prompt_message = {'role': 'user', 'content': prompt}
    appended_history = [prompt_message]
    if system:
        appended_history += [{'role': 'system', 'content': system}]
    response = ollama.chat(model, history+appended_history, format=format, options=options)
    print(response)
    if format == 'json':
        try:
            return json.loads(response['message']['content'])
        except:
            return ochat(model, prompt, history, save_prompt, save_response, format, options, system)
    if save_prompt:
        history.append(prompt_message)
    if save_response:
        history.append(response['message'])
    return response['message']['content']