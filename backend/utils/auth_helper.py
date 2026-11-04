from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def role_required(allowed_roles):
    """Decorator to restrict access based on user role."""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request() # This checks if a valid token is provided
            claims = get_jwt()
            user_role = claims.get("role")
            
            if user_role not in allowed_roles:
                return jsonify({"error": "Access forbidden: insufficient permissions"}), 403
                
            return fn(*args, **kwargs)
        return decorator
    return wrapper