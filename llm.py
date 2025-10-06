from dotenv import load_dotenv
from openai import AzureOpenAI
import os
from pathlib import Path

load_dotenv()

class AZURE_OPENAI_Config:
    api_key = os.getenv('AZURE_OPENAI_API_KEY')
    api_version = os.getenv('AZURE_OPENAI_API_VERSION')
    api_endpoint = os.getenv('AZURE_OPENAI_API_END_POINT')

    def __init__(self):
        if not all([self.api_key, self.api_version, self.api_endpoint]):
            raise ValueError('Missing Required Azure OpenAI environment variables.')
        
class Label(AZURE_OPENAI_Config):
    def __init__(self, context_prompt_path:Path, llm_deployed_model:str='gpt-4o-t1'):
        super().__init__()
        self.context_prompt_path = context_prompt_path
        self.llm_model = llm_deployed_model
        self.client = self._client()
        self.context_prompt = self._get_context_prompt()

    def _get_context_prompt(self) -> str:
        if not isinstance(self.context_prompt_path, Path):
            raise ValueError("Context Prompt Path must be in a pathlib.Path")
        
        with self.context_prompt_path.open('r', encoding='utf-8') as f:
            return self.context_prompt_path.read_text(encoding='utf-8')

    def _client(self):
        return AzureOpenAI(
            api_key = self.api_key,
            api_version = self.api_version,
            azure_endpoint = self.api_endpoint
        )

    def run(self, base64_image):
        response = self.client.chat.completions.create(
            model=self.llm_model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": self.context_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
        )


        return response.choices[0].message.content