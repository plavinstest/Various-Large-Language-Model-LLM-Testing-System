from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from together import Together
import uuid
from LLM_chatting_app.models import user_prompts_record, prompt_response_with_models

# Initialize the Together client with the required API key
client = Together(api_key="")

import openai
# Set up OpenAI API key for GPT model interactions
openai.api_key = ''



@csrf_exempt
def index(request):
    """
    Renders the homepage and handles user interactions.
    - POST: Processes user prompts, selects models, and stores the results.
    - GET: Initializes a session and renders the homepage.
    """
    if request.method == 'POST':
        # Retrieve user input and session information
        message = request.POST.get("message")
        request.session['message'] = message
        model_number = int(request.POST.get("model"))
        session_id = request.session['session_id']
        # Route to the appropriate chat function based on the selected model
        if model_number in [8, 9, 10]:
            status, answer, model_name = chat_with_gpt(message, model_number)
            
        else:

            status, answer, model_name = chat_with_LLM(message, model_number)
        model_name = model_name.capitalize()
        # Store prompt and response in the database if successful
        if status == 'success':
            obj_user_prompts_record, created = user_prompts_record.objects.get_or_create(
                user_prompt=message,
                defaults={
                    'session_id': session_id
                    # 'description': description
                }
            )
            obj_prompt_response_with_models, created = prompt_response_with_models.objects.get_or_create(
                user_prompts=obj_user_prompts_record,
                answer=answer,
                model=model_name
            )
        # Return the chat response as JSON
        context = {
            "status": status,
            "answer": answer
        }
        return JsonResponse(context)
    else:
        # Initialize session for GET requests and render the homepage
        message = request.session.pop('message', None)
        session_id = str(uuid.uuid4())
        request.session['session_id'] = session_id
        return render(request, "index.html")


def chat_with_LLM(prompt, model_number):
    """
    Handles interaction with non-GPT LLM models via Together API.
    - Sends the user prompt to the selected model.
    - Returns the model's response.
    """
    models = [
        "meta-llama/Llama-3.2-3B-Instruct-Turbo",
        "google/gemma-2b-it",
        "mistralai/Mistral-7B-Instruct-v0.3",
        "Qwen/Qwen2.5-7B-Instruct-Turbo",
        "Gryphe/MythoMax-L2-13b",
        "deepseek-ai/deepseek-llm-67b-chat",
        "upstage/SOLAR-10.7B-Instruct-v1.0",
        "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"  # Free model
    ]
    # Loop through models and generate responses
    # for model1 in models:
    model1 = models[model_number]
    try:
        # Call the Together API to generate a response
        # response = client.complete(
        #     model=model,
        #     prompt=prompt,
        #     max_tokens=100
        # )
        response = client.chat.completions.create(
            model=model1,
            messages=[{"role": "user", "content": prompt}], )
        print(f"Response from {model1}:")
        print(response.choices[0].message.content)
        print("\n" + "-" * 50 + "\n")
        response_message = response.choices[0].message.content
        return "success", response_message, model1
    except Exception as e:
        # Handle errors during model interaction
        print(f"Error with model {model1}: {e}")
        return "failed", None, model1


def chat_with_gpt(prompt, model_number):
    """
    Handles interaction with GPT models via OpenAI API.
    - Sends the user prompt to the selected GPT model.
    - Returns the model's response.
    """
    models = [
        "meta-llama/Llama-3.2-3B-Instruct-Turbo",
        "google/gemma-2b-it",
        "mistralai/Mistral-7B-Instruct-v0.3",
        "Qwen/Qwen2.5-7B-Instruct-Turbo",
        "Gryphe/MythoMax-L2-13b",
        "deepseek-ai/deepseek-llm-67b-chat",
        "upstage/SOLAR-10.7B-Instruct-v1.0",
        "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "gpt-3.5-turbo",
        "gpt-4-turbo"
        
    ]

    model = models[model_number]
    try:
        # Call the OpenAI API to generate a response
        response = openai.ChatCompletion.create(
            model=model,  # You can use "gpt-3.5-turbo" or "gpt-4"
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        # Extract the response text
        answer = response['choices'][0]['message']['content'].strip()
        return 'success', answer, model
    except Exception as e:
        # Handle errors during GPT interaction
        print(f"Error: {e}")
        return 'failed', None, model

# def chat_with_Gpt(prompt, model_number):
#     # Define your prompt
#     # prompt = "Tell me about sustainable energy solutions."
#     # Example usage with different models
#     # List of updated models with correct API model strings
#     models = [
#         "meta-llama/Llama-3.2-3B-Instruct-Turbo",
#         "google/gemma-2b-it",
#         "mistralai/Mistral-7B-Instruct-v0.3",
#         "Qwen/Qwen2.5-7B-Instruct-Turbo",
#         "Gryphe/MythoMax-L2-13b",
#         "deepseek-ai/deepseek-llm-67b-chat",
#         "upstage/SOLAR-10.7B-Instruct-v1.0",
#         "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"  # Free model
#         "chatgpt-4o-"
#         "chatgpt-3.5"
#         "chatgpt-4o-mini"
#
#     ]
#     # Loop through models and generate responses
#     # for model1 in models:
#     model1 = models[model_number]
#     try:
#         # response = client.complete(
#         #     model=model,
#         #     prompt=prompt,
#         #     max_tokens=100
#         # )
#         response = client.chat.completions.create(
#             model=model1,
#             messages=[{"role": "user", "content": prompt}], )
#         print(f"Response from {model1}:")
#         print(response.choices[0].message.content)
#         print("\n" + "-" * 50 + "\n")
#         response_message = response.choices[0].message.content
#         return "success", response_message, model1
#     except Exception as e:
#         print(f"Error with model {model1}: {e}")
#         return "failed", None, model1
    


def result(request):
    """
    Displays chat history and corresponding model responses.
    - Fetches the latest user prompts and responses from the database.
    """
    # message = request.session.get('message')
    message = "Hello"
    user_result = []
    if message is not None:
        try:
            # Retrieve the latest 30 prompts and responses
            # obj_user_prompts_record = user_prompts_record.objects.get(user_prompt=message)
            obj_user_prompts_record = user_prompts_record.objects.all().order_by('-id')[:30]
            for prompts_record in obj_user_prompts_record:
                obj_prompt_response_with_models = prompt_response_with_models.objects.filter(user_prompts=prompts_record)
                # if len(obj_prompt_response_with_models) > 0:
                for i in obj_prompt_response_with_models:
                    user_prompt = i.user_prompts.user_prompt
                    model_name = i.model
                    answer = i.answer
                    id = i.id
                    data_dict = {
                        "id": id,
                        "user_prompt": user_prompt,
                        "model_name": model_name,
                        "answer": answer
                    }
                    user_result.append(data_dict)
        except user_prompts_record.DoesNotExist:
            pass
    if len(user_result) > 0:
        data_count = len(user_result)
        context = {
            "user_result": user_result,
            "data_count": data_count
        }
    else:
        context = {
            "user_result": user_result,
        }
    print(user_result)
    return render(request, "result.html", context)


@csrf_exempt
def delete_message(request):
    if request.method == 'POST':
        message_id = request.POST.get('id')
        try:
            # Attempt to delete the message
            message = prompt_response_with_models.objects.get(id=message_id)
            message.delete()
            return JsonResponse({'success': True})
        except prompt_response_with_models.DoesNotExist:
            # Handle case where message ID does not exist
            return JsonResponse({'success': False, 'error': 'Message not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

