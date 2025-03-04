import unittest
from unittest.mock import patch, MagicMock
import os
import platform
from llm import BaseLLM, OpenAILLM, GeminiLLM

class TestBaseLLM(unittest.TestCase):
    def setUp(self):
        self.model_name = "test-model"
        self.base_llm = BaseLLM(self.model_name)

    def test_init(self):
        """Test initialization of BaseLLM"""
        self.assertEqual(self.base_llm.model_name, self.model_name)
        self.assertIsNotNone(self.base_llm.system_instruction)

    def test_system_instruction_content(self):
        """Test system instruction contains required information"""
        instruction = self.base_llm.get_system_instruction()
        self.assertIn(self.model_name, instruction)
        self.assertIn(platform.system(), instruction)
        self.assertIn(os.environ.get('SHELL', 'Unknown Shell'), instruction)
        self.assertIn(os.getcwd(), instruction)

    def test_call_not_implemented(self):
        """Test that call method raises NotImplementedError"""
        with self.assertRaises(NotImplementedError):
            self.base_llm.call("test prompt")

class TestOpenAILLM(unittest.TestCase):
    @patch('openai.OpenAI')
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def setUp(self, mock_openai):
        """Set up test case with mocked OpenAI"""
        self.mock_openai = mock_openai
        self.openai_llm = OpenAILLM()

    def test_init(self):
        """Test initialization of OpenAILLM"""
        self.assertEqual(self.openai_llm.model_name, "gpt-4o")
        self.assertIsNotNone(self.openai_llm.client)

    @patch('openai.OpenAI')
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_call(self, mock_openai_class):
        """Test OpenAI call method"""
        # Set up mock client and response
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_message = MagicMock()
        mock_message.content = "Test response"
        mock_choice = MagicMock()
        mock_choice.message = mock_message
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        
        mock_client.chat.completions.create.return_value = mock_response

        # Create LLM instance and make call
        llm = OpenAILLM()
        response = llm.call("test prompt")
        
        # Verify response and API call
        self.assertEqual(response, "Test response")
        mock_client.chat.completions.create.assert_called_once()
        
        # Verify correct parameters were passed
        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        self.assertEqual(call_kwargs['model'], "gpt-4o")
        self.assertEqual(len(call_kwargs['messages']), 2)
        self.assertEqual(call_kwargs['messages'][0]['role'], "system")
        self.assertEqual(call_kwargs['messages'][1]['role'], "user")
        self.assertEqual(call_kwargs['messages'][1]['content'], "test prompt")

class TestGeminiLLM(unittest.TestCase):
    @patch('google.generativeai.GenerativeModel')
    @patch('google.generativeai.configure')
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'})
    def setUp(self, mock_configure, mock_model_class):
        """Set up test case with mocked Gemini"""
        self.mock_model_class = mock_model_class
        self.mock_configure = mock_configure
        self.gemini_llm = GeminiLLM()

    def test_init(self):
        """Test initialization of GeminiLLM"""
        self.assertEqual(self.gemini_llm.model_name, "gemini-1.5-flash")
        self.assertIsNotNone(self.gemini_llm.model)
        self.mock_configure.assert_called_once_with(api_key='test_key')

    @patch('google.generativeai.GenerativeModel')
    @patch('google.generativeai.configure')
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'})
    def test_call(self, mock_configure, mock_model_class):
        """Test Gemini call method"""
        # Set up mock model and response
        mock_model = MagicMock()
        mock_model_class.return_value = mock_model
        
        mock_response = MagicMock()
        mock_response.text = "Test response"
        mock_model.generate_content.return_value = mock_response

        # Create LLM instance and make call
        llm = GeminiLLM()
        response = llm.call("test prompt")
        
        # Verify response and API call
        self.assertEqual(response, "Test response")
        mock_model.generate_content.assert_called_once_with("test prompt")
        
        # Verify model was initialized with correct parameters
        mock_model_class.assert_called_once()
        model_args = mock_model_class.call_args
        self.assertEqual(model_args[0][0], "gemini-1.5-flash")
        self.assertIn('system_instruction', model_args[1])

if __name__ == '__main__':
    unittest.main() 