from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock
from LLM_chatting_app.models import user_prompts_record, prompt_response_with_models
import uuid

# Test cases for the User Interaction module
class UserInteractionTests(TestCase):
    def setUp(self):
        # Initializes a test client and session for user interaction
        self.client = Client()
        session = self.client.session
        session['session_id'] = str(uuid.uuid4())
        session.save()

    def test_select_llm_from_dropdown(self):
        # Verifies that the dropdown for LLM selection is present on the index/homepage
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<select name="models_name"')

    def test_send_prompt_to_ai_model(self):
        # Checks that a prompt can be submitted and processed successfully
        response = self.client.post(reverse('index'), {
            'message': 'Test prompt',
            'model': '0',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('answer', response.json())


# Test cases for AI Integration module
class AIIntegrationTests(TestCase):
    @patch('LLM_chatting_app.views.client.chat.completions.create')
    def test_process_prompt_with_llm(self, mock_create):
        # Simulates a successful LLM response using a mock API
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content='Mocked LLM Response'))]
        mock_create.return_value = mock_response

        from LLM_chatting_app.views import chat_with_LLM
        status, answer, model_name = chat_with_LLM("Test prompt", 0)

        self.assertEqual(status, "success")
        self.assertEqual(answer, "Mocked LLM Response")
        self.assertEqual(model_name, "meta-llama/Llama-3.2-3B-Instruct-Turbo")

    @patch('openai.ChatCompletion.create')
    def test_handle_api_response(self, mock_create):
        # Simulates handling a valid GPT API response
        mock_create.return_value = {
            'choices': [{'message': {'content': 'Mocked GPT Response'}}]
        }

        from LLM_chatting_app.views import chat_with_gpt
        status, answer, model_name = chat_with_gpt("Test prompt", 8)

        self.assertEqual(status, "success")
        self.assertEqual(answer, "Mocked GPT Response")
        self.assertEqual(model_name, "gpt-3.5-turbo")

    @patch('LLM_chatting_app.views.client.chat.completions.create')
    def test_llm_api_failure(self, mock_create):
        # Simulates an API failure and verifies proper error handling
        mock_create.side_effect = Exception("Mocked API failure")

        from LLM_chatting_app.views import chat_with_LLM
        status, answer, model_name = chat_with_LLM("Test prompt", 0)

        self.assertEqual(status, "failed")
        self.assertIsNone(answer)
        self.assertEqual(model_name, "meta-llama/Llama-3.2-3B-Instruct-Turbo")


# Test cases for Database Management module
class DatabaseManagementTests(TestCase):
    def setUp(self):
        # Sets up test data for database management tests
        self.session_id = str(uuid.uuid4())
        self.prompt = user_prompts_record.objects.create(
            session_id=self.session_id,
            user_id=1,
            user_prompt='Test prompt',
        )
        self.response = prompt_response_with_models.objects.create(
            user_prompts=self.prompt,
            answer='Test answer',
            model='Test Model'
        )

    def test_save_user_prompt(self):
        # Confirms that user prompts are saved correctly
        self.assertEqual(user_prompts_record.objects.count(), 1)
        self.assertEqual(self.prompt.user_prompt, 'Test prompt')

    def test_retrieve_chat_history(self):
        # Ensures that chat history can be retrieved successfully
        history = user_prompts_record.objects.all()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].user_prompt, 'Test prompt')

    def test_delete_specific_chat_entry(self):
        # Tests the deletion of a specific chat entry
        self.response.delete()
        self.assertEqual(prompt_response_with_models.objects.count(), 0)

    def test_delete_nonexistent_entry(self):
        # Ensures no errors occur when attempting to delete a nonexistent entry
        response = prompt_response_with_models.objects.filter(id=999).delete()
        self.assertEqual(response[0], 0)


# Test cases for Results Management module
class ResultsManagementTests(TestCase):
    def setUp(self):
        # Seting up test data for results management tests
        self.session_id = str(uuid.uuid4())
        self.prompt = user_prompts_record.objects.create(
            session_id=self.session_id,
            user_id=1,
            user_prompt='Test prompt',
        )
        prompt_response_with_models.objects.create(
            user_prompts=self.prompt,
            answer='Test answer',
            model='Test Model'
        )

    def test_load_chat_history(self):
        # Verifies that chat history is correctly loaded in the results view
        response = self.client.get(reverse('result'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test prompt')

    def test_export_chat_history_content(self):
        # Checks that chat history content is present for export functionality
        response = self.client.get(reverse('result'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, '<div class="content">Test prompt</div>')
        self.assertContains(response, '<div class="content">Test answer</div>')

    def test_export_empty_chat_history(self):
        # Ensures no errors occur when exporting an empty chat history
        user_prompts_record.objects.all().delete()
        response = self.client.get(reverse('result'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, '<div class="content">Test prompt</div>')
