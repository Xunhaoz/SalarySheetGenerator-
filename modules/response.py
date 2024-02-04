class Response:
    @staticmethod
    def not_found(e):
        return {"response": "not_found", "message": str(e)}, 404

    @staticmethod
    def sever_error(e):
        return {"response": "sever_error", "message": str(e)}, 500

    @staticmethod
    def client_error(e):
        return {"response": "client_error", "message": str(e)}, 400

    @staticmethod
    def response(obj: str or dict):
        return {"response": "success", "message": obj}, 200
