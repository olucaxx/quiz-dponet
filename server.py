from http.server import BaseHTTPRequestHandler, HTTPServer
import json, os

PORT: int = 8080
QUESTIONS_DIR: str = os.path.join(os.path.dirname(__file__), 'questoes')
ROUTES: dict = {
    '/questions/culturaEtica': 'culturaEtica.json',
    '/questions/gestaoPessoasRH': 'gestaoPessoasRH.json',
    '/questions/legalidadeRegulacao': 'legalidadeRegulacao.json',
    '/questions/marketingVendas': 'marketingVendas.json',
    '/questions/processosGovernanca': 'processosGovernanca.json',
    '/questions/tecnologiaSeguranca': 'tecnologiaSeguranca.json'
}
CATEGORIES: dict = {
    'Cultura e Ética': 'culturaEtica.json',
    'Gestão de Pessoas e RH': 'gestaoPessoasRH.json',
    'Legalidade e Regulação': 'legalidadeRegulacao.json',
    'Marketing e Vendas': 'marketingVendas.json',
    'Processos e Governança': 'processosGovernanca.json',
    'Tecnologia e Segurança': 'tecnologiaSeguranca.json'
}

class QuizRequestHandler(BaseHTTPRequestHandler):         
    def _send_json_response(self, data: dict[str, str], status_code: int) -> None:
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json') 
        self.send_header('Access-Control-Allow-Origin', '*') 
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2, ensure_ascii=False).encode())
    
    def _send_error(self, message: str, status_code:int) -> None:
        self.send_response(status_code)
        self.end_headers()
        self.wfile.write(f"Error {status_code} - {message}".encode())
        
    
    def do_GET(self) -> None:
        if self.path not in ROUTES:
            self._send_error('Endpoint not found', 404)
            return

        try:
            json_path: str = os.path.join(QUESTIONS_DIR, ROUTES[self.path])
            
            with open(json_path, 'r', encoding='utf-8') as file:
                raw_questions: dict = json.load(file)
                
            response_data: dict = {
                "categoria": raw_questions["categoria"],
                "questoes": [
                    {
                        "id_questao": raw_question["id_questao"],
                        "questao": raw_question["questao"],
                        "respostas": raw_question["respostas"]
                    }
                    for raw_question in raw_questions["questoes"]
                ]
            }
            
            self._send_json_response(response_data, 200)

        except FileNotFoundError:
            self._send_error('Internal Error: Missing files', 500)
    
        except Exception as e:
            self._send_error(bytes(f'Internal Error: {str(e)}'.encode()), 500)
            
    def do_POST(self) -> None:
        if self.path != '/user-answers':
            self._send_error('Endpoint not found', 404)
            return
        
        try:
            content_length: int = int(self.headers['Content-Length'])
            post_data: bytes = self.rfile.read(content_length)
            
            answers: dict = json.loads(post_data.decode('utf-8'))
            
            if 'categoria' not in answers :
                self._send_error('Invalid JSON format, missing "categoria"', 400)
                return
            
            if 'respostas' not in answers:
                self._send_error('Invalid JSON format, missing "respostas"', 400)
                return
            
            if answers['categoria'] not in CATEGORIES:
                self._send_error('Invalid "categoria"', 400)
                return
            
            json_path: str = os.path.join(QUESTIONS_DIR, CATEGORIES[answers['categoria']])
            
            with open(json_path, 'r', encoding='utf-8') as file:
                correct_answers_dict: dict = json.load(file)
             
            
            self._send_json_response({'teste': 'teste'}, 200)
            
        except json.JSONDecodeError:
            self._send_error('Invalid JSON', 400)
        
        
        # except Exception as e:
        #     self._send_error(f'Internal Error: {str(e)}'.encode(), 500)
        
def run():
    server_address = ("", PORT)
    httpd = HTTPServer(server_address, QuizRequestHandler)
    print(f"Server running on port {PORT}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
    
"""
exemplo de POST desejado:

{
    "categoria": "Tecnologia e Segurança",
    "respostas": [
        {
            "id_questao": 1,
            "id_resposta": 2
        },
        {
            "id_questao": 2,
            "id_resposta": 3
        },
        {
            "id_questao": 3,
            "id_resposta": 2
        },
        {
            "id_questao": 4,
            "id_resposta": 1
        },
        {
            "id_questao": 5,
            "id_resposta": 4
        },
        {
            "id_questao": 6,
            "id_resposta": 2
        },
        {
            "id_questao": 7,
            "id_resposta": 1
        },
        {
            "id_questao": 8,
            "id_resposta": 2
        },
        {
            "id_questao": 9,
            "id_resposta": 2
        },
        {
            "id_questao": 10,
            "id_resposta": 2
        },
        {
            "id_questao": 11,
            "id_resposta": 2
        },
        {
            "id_questao": 12,
            "id_resposta": 4
        },
        {
            "id_questao": 13,
            "id_resposta": 2
        },
        {
            "id_questao": 14,
            "id_resposta": 2
        },
        {
            "id_questao": 15,
            "id_resposta": 3
        }
    ]
}
"""