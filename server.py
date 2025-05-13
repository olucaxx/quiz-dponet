from http.server import BaseHTTPRequestHandler, HTTPServer
import json, os

class QuizRequestHandler(BaseHTTPRequestHandler):
    def get_json_path(self, url_path: str) -> str:
        root_path: str = os.path.join(os.path.dirname(__file__), 'questoes')
        
        match url_path:
            case '/questions/culturaEtica':
                return os.path.join(root_path, 'culturaEtica.json')
            
            case '/questions/gestaoPessoasRH':
                return os.path.join(root_path, 'gestaoPessoasRH.json')
            
            case '/questions/legalidadeRegulacao':
                return os.path.join(root_path, 'legalidadeRegulacao.json')
            
            case '/questions/marketingVendas':
                return os.path.join(root_path, 'marketingVendas.json')
            
            case '/questions/processosGovernanca':
                return os.path.join(root_path, 'processosGovernanca.json')
            
            case '/questions/tecnologiaSeguranca':
                return os.path.join(root_path, 'tecnologiaSeguranca.json')
            
            case _:
                return ""
            
    def load_questions_dict(self, questions_path: str) -> dict:
        with open(questions_path, 'r', encoding='utf-8') as file:
                raw_questions: dict = json.load(file)
                
        return {
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
    
    def do_GET(self):
        questions_path: str = self.get_json_path(self.path)
        
        if not questions_path:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Endpoint not found')
            return

        try:
            questions: dict = self.load_questions_dict(questions_path)
            self.send_response(200)
            self.send_header('Content-type', 'application/json') 
            self.send_header('Access-Control-Allow-Origin', '*') 
            self.end_headers()
            self.wfile.write(json.dumps(questions)).encode() 
            
        except FileNotFoundError:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'File not found')
        
def run():
    server_address = ("", 8080)
    httpd = HTTPServer(server_address, QuizRequestHandler)
    print("Server running...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()