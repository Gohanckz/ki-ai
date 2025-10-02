"""
Ollama Client - Interface for local LLM inference
"""

import ollama
from typing import Dict, List, Optional, Generator
from pathlib import Path

from backend.utils.logger import setup_logger
from backend.utils.config import settings

logger = setup_logger("ki.ml.ollama")


class OllamaClient:
    """Client for interacting with Ollama LLM"""

    def __init__(self, host: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize Ollama client

        Args:
            host: Ollama server URL (defaults to settings)
            model: Default model to use (defaults to settings)
        """
        self.host = host or settings.ollama_host
        self.model = model or settings.ollama_model

        # Configure Ollama client
        if self.host != "http://localhost:11434":
            # Set custom host if not default
            ollama._client.DEFAULT_HOST = self.host

        logger.info(f"Ollama client initialized: {self.host}, model: {self.model}")

    def is_available(self) -> bool:
        """
        Check if Ollama server is available

        Returns:
            True if server is reachable, False otherwise
        """
        try:
            # Try to list models
            ollama.list()
            logger.info("✅ Ollama server is available")
            return True
        except Exception as e:
            logger.error(f"❌ Ollama server not available: {str(e)}")
            return False

    def list_models(self) -> List[str]:
        """
        Get list of available models

        Returns:
            List of model names
        """
        try:
            models = ollama.list()
            model_names = [model['name'] for model in models.get('models', [])]
            logger.info(f"Available models: {model_names}")
            return model_names
        except Exception as e:
            logger.error(f"Error listing models: {str(e)}")
            return []

    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        stream: bool = False
    ) -> str:
        """
        Generate text from prompt

        Args:
            prompt: Input prompt
            model: Model to use (defaults to self.model)
            temperature: Sampling temperature (0.0 to 2.0)
            max_tokens: Maximum tokens to generate
            stream: Whether to stream response

        Returns:
            Generated text
        """
        model = model or self.model

        try:
            logger.info(f"Generating with model: {model}")

            response = ollama.generate(
                model=model,
                prompt=prompt,
                options={
                    'temperature': temperature,
                    'num_predict': max_tokens
                },
                stream=stream
            )

            if stream:
                return response
            else:
                generated_text = response['response']
                logger.info(f"✅ Generated {len(generated_text)} characters")
                return generated_text

        except Exception as e:
            logger.error(f"❌ Generation error: {str(e)}")
            return f"Error: {str(e)}"

    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        stream: bool = False
    ) -> str:
        """
        Chat with model using message history

        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model to use (defaults to self.model)
            temperature: Sampling temperature
            stream: Whether to stream response

        Returns:
            Model response
        """
        model = model or self.model

        try:
            logger.info(f"Chat with model: {model}, messages: {len(messages)}")

            response = ollama.chat(
                model=model,
                messages=messages,
                options={'temperature': temperature},
                stream=stream
            )

            if stream:
                return response
            else:
                reply = response['message']['content']
                logger.info(f"✅ Chat response: {len(reply)} characters")
                return reply

        except Exception as e:
            logger.error(f"❌ Chat error: {str(e)}")
            return f"Error: {str(e)}"

    def generate_examples_from_text(
        self,
        text: str,
        category: str,
        num_examples: int = 5,
        temperature: float = 0.7
    ) -> List[Dict[str, str]]:
        """
        Generate training examples from text content

        Args:
            text: Source text to generate examples from
            category: Vulnerability category (SSRF, XSS, etc.)
            num_examples: Number of examples to generate
            temperature: Sampling temperature

        Returns:
            List of example dictionaries with instruction/input/output
        """
        prompt = f"""You are an expert in cybersecurity and bug bounty hunting, specializing in {category} vulnerabilities.

Given the following text content, generate {num_examples} high-quality training examples for teaching AI agents about {category}.

Each example should follow this exact JSON format:
{{
  "instruction": "A clear task instruction",
  "input": "Specific context or scenario",
  "output": "Detailed explanation or analysis of the {category} vulnerability"
}}

Text content:
{text[:4000]}

Generate {num_examples} diverse, educational examples focusing on different aspects of {category}. Output only valid JSON array.
"""

        try:
            response = self.generate(
                prompt=prompt,
                temperature=temperature,
                max_tokens=4096
            )

            # Parse JSON response
            import json
            examples = json.loads(response)

            if isinstance(examples, list):
                logger.info(f"✅ Generated {len(examples)} examples for {category}")
                return examples
            else:
                logger.warning("Response is not a list, wrapping in array")
                return [examples]

        except json.JSONDecodeError as e:
            logger.error(f"❌ Failed to parse JSON: {str(e)}")
            # Return placeholder examples
            return [{
                "instruction": f"Analyze this {category} scenario",
                "input": "Sample input from document",
                "output": "This is a placeholder example. JSON parsing failed.",
                "error": str(e)
            }]
        except Exception as e:
            logger.error(f"❌ Example generation error: {str(e)}")
            return []

    def stream_generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7
    ) -> Generator[str, None, None]:
        """
        Stream generation token by token

        Args:
            prompt: Input prompt
            model: Model to use
            temperature: Sampling temperature

        Yields:
            Generated tokens
        """
        model = model or self.model

        try:
            stream = ollama.generate(
                model=model,
                prompt=prompt,
                options={'temperature': temperature},
                stream=True
            )

            for chunk in stream:
                if 'response' in chunk:
                    yield chunk['response']

        except Exception as e:
            logger.error(f"❌ Streaming error: {str(e)}")
            yield f"Error: {str(e)}"

    def pull_model(self, model_name: str) -> bool:
        """
        Pull/download a model from Ollama registry

        Args:
            model_name: Name of model to pull

        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Pulling model: {model_name}")
            ollama.pull(model_name)
            logger.info(f"✅ Model {model_name} pulled successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to pull model {model_name}: {str(e)}")
            return False

    def get_model_info(self, model_name: Optional[str] = None) -> Dict:
        """
        Get information about a model

        Args:
            model_name: Name of model (defaults to self.model)

        Returns:
            Model information dictionary
        """
        model_name = model_name or self.model

        try:
            info = ollama.show(model_name)
            logger.info(f"Model info retrieved: {model_name}")
            return info
        except Exception as e:
            logger.error(f"❌ Failed to get model info: {str(e)}")
            return {"error": str(e)}


# Global client instance
ollama_client = OllamaClient()


def get_ollama_client(host: Optional[str] = None, model: Optional[str] = None) -> OllamaClient:
    """
    Get Ollama client instance

    Args:
        host: Optional custom host
        model: Optional custom model

    Returns:
        OllamaClient instance
    """
    if host or model:
        return OllamaClient(host=host, model=model)
    return ollama_client
