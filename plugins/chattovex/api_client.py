# /home/johnb/tasma-code-absulut/plugins/chattovex/api_client.py
import json
import urllib.request
import urllib.error

class GroqClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.3-70b-versatile" # Modelo atualizado

    def send_message(self, messages, temperature=0.7):
        """Envia mensagens para a API e retorna a resposta."""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature
        }
        
        try:
            req = urllib.request.Request(
                self.api_url, 
                data=json.dumps(data).encode('utf-8'), 
                headers=headers
            )
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result['choices'][0]['message']['content']
        except urllib.error.HTTPError as e:
            try:
                error_body = e.read().decode('utf-8')
                return f"Erro API: {e.code} - {error_body}"
            except:
                return f"Erro API: {e.code} - {e.reason}"
        except Exception as e:
            return f"Erro: {str(e)}"
