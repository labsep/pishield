from google import genai
from google.genai import types
from google.genai.errors import ServerError
import json

class Agente:
    def __init__(self, chave, instrucao_sistema):
        self.cliente = genai.Client(api_key=chave)
        self.instrucao_sistema = instrucao_sistema

    def analisar_vulnerabilidade(self, vulnerabilidade, tentativa=False):
        try:
            resposta = self.cliente.models.generate_content(
                model="gemini-2.0-flash",
                config=types.GenerateContentConfig(
                    system_instruction=self.instrucao_sistema
                ),
                contents=json.dumps(vulnerabilidade, ensure_ascii=False, indent=2)
            )
        except ServerError as e:
            if e.code == 503 and not tentativa:
                return self.analisar_vulnerabilidade(vulnerabilidade, tentativa=True)
            raise

        return resposta.text
    