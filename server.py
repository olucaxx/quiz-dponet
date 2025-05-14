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
        self.wfile.write(message)
        
    
    def do_GET(self) -> None:
        if self.path not in ROUTES:
            self._send_error(b'Endpoint not found', 404)
            return

        try:
            json_path: str = os.path.join(QUESTIONS_DIR, ROUTES[self.path])
            
            with open(json_path, 'r', encoding='utf-8') as file:
                raw_questions: dict = json.load(file)
                
            response_data = {
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
            self._send_error(b'File not found', 500)
        
def run():
    server_address = ("", PORT)
    httpd = HTTPServer(server_address, QuizRequestHandler)
    print(f"Server running on port {PORT}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()