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
    def _set_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
    def _send_json_response(self, data: dict, status_code: int) -> None:
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json') 
        self.send_header('Access-Control-Allow-Origin', '*') 
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
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
                questions: dict = json.load(file)
                
            response_data: dict = {
                "categoria": questions["categoria"],
                "questoes": [
                    {
                        "id_questao": q["id_questao"],
                        "questao": q["questao"],
                        "respostas": q["respostas"]
                    }
                    for q in questions["questoes"]
                ]
            }

            self._send_json_response(response_data, 200)

        except FileNotFoundError:
            self._send_error('Internal Error: Missing files', 500)
    
        except Exception as e:
            self._send_error(bytes(f'Internal Error: {str(e)}'.encode()), 500)
            
    def do_OPTIONS(self) -> None:
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()
    
    def do_POST(self) -> None:
        if self.path != '/user-answers':
            self._send_error('Endpoint not found', 404)
            return
        
        try:
            content_length: int = int(self.headers['Content-Length'])
            post_data: bytes = self.rfile.read(content_length)
            
            answers: dict = json.loads(post_data.decode())

            if 'categoria' not in answers:
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
                questions: dict = json.load(file)

            correct_answers: dict = { q["id_questao"]: q["id_resposta"] for q in questions["questoes"] }
                
            score: int = 0

            for answer in answers['respostas']:
                question_id = int(answer['id_questao'])
                answer_id = int(answer['id_resposta'])
                
                if question_id in correct_answers and answer_id == correct_answers[question_id]:
                    score += 1
            
            self._send_json_response({"acertos": score}, 200)
            
        except json.JSONDecodeError:
            self._send_error('Invalid JSON', 400)
        
        except Exception as e:
            self._send_error(f'Internal Error: {str(e)}'.encode(), 500)
        
def run():
    server_address = ("", PORT)
    httpd = HTTPServer(server_address, QuizRequestHandler)
    print(f"Server running on port {PORT}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
    