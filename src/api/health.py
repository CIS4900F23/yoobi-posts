from flask_restx import Namespace, Resource

# Create an API namespace for our health operations
api = Namespace("health", description="Health check related operations")

class Health(Resource):
    """_summary_

    Args:
        Resource (_type_): _description_
    """
    def get(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return {"status": "OK", "message": "Server is healthy"}

api.add_resource(Health, "")