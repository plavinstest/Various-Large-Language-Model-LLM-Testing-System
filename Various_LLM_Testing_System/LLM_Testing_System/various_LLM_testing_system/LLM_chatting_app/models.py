from django.db import models

# Defining the database models for the LLM Chatting Application

class user_prompts_record(models.Model):
    # Field to store the session ID associated with the user
    session_id = models.TextField(default='')
    # Field to represent the user ID
    user_id = models.IntegerField(default=0)
    # Field to store the prompt entered by the user
    user_prompt = models.TextField(default='')
    # Timestamp to record when the prompt was created
    created_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)

class prompt_response_with_models(models.Model):
    # ForeignKey linking this response to a specific user prompt
    user_prompts = models.ForeignKey(user_prompts_record, on_delete=models.CASCADE)
    # Field to store the generated response from the LLM
    answer = models.TextField(default='')
    # Field to store the model used to generate the response
    model = models.CharField(default='', max_length=256)
    # Timestamp to record when the response was created
    created_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
