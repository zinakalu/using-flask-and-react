from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from config import DevConfig
from models import Recipe, User
from exts import db
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token


app=Flask(__name__)
app.config.from_object(DevConfig)

db.init_app(app)


migrate=Migrate(app,db)
JWTManager(app)

api=Api(app,doc='/docs')


#model(serializer)
recipe_model=api.model(
    "Recipe",
    {
        "id":fields.Integer(),
        "title":fields.String(),
        "description":fields.String()
    }
)


signup_model=api.model(
    'Signup',
    {
        "username":fields.String(),
        "email":fields.String(),
        "password":fields.String()
    }
)

login_model=api.model(
    'Login',
    {
        "username":fields.String(),
        "password":fields.String()
    }
)

@api.route('/hello')
class HelloResource(Resource):
    def get(self):
        return {"message": "Hello World"}
# @app.route('/hello')
# def hello():
#     return {"message":"Hello World"}

@api.route('/signup')
class SignUp(Resource):
    # @api.marshal_with(signup_model)
    @api.expect(signup_model)
    def post(self):
        data = request.get_json()

        # new_user=User(
        #     username=data.get('username'),
        #     email=data.get('email'),
        #     password=data.get('password')
        # )
        
        # new_user.save()
        # return new_user.to_dict(), 201
        db_user=User.query.filter_by(username=data.get('username')).first()

        if db_user is not None:
            return {"message": f"User with username {data.get('username')} already exists"}, 409

        new_user=User(
            username=data.get('username'),
            email=data.get('email'),
            password=generate_password_hash(data.get('password'))
        )

        new_user.save()

        return {"message": "User created successfully", 'user': new_user.to_dict()}, 201



    

@api.route('/login')
class Login(Resource):

    @api.expect(login_model)
    def post(self):
        data=request.get_json()
        username=data.get('username')
        password=data.get('password')

        db_user=User.query.filter_by(username=username).first()

        if db_user and check_password_hash(db_user.password, password):
            access_token=create_access_token(identity=db_user.username)
            refresh_token=create_refresh_token(identity=db_user.username)

            return jsonify(
                {"access_token": access_token, "refresh_token":refresh_token}
            )
        else:
            return ({"message": "Invalid credentials"}), 401




@api.route('/recipes')
class RecipesResource(Resource):

    @api.marshal_list_with(recipe_model)
    def get(self):
        """
        Get all recipes
        """
        recipes=Recipe.query.all() #returns a list of recipes

        return recipes #returning the list of recipes

    @api.marshal_with(recipe_model)
    @api.expect(recipe_model)
    def post(self):
        """Create a new recipe"""
        data=request.get_json()

        new_recipe=Recipe(
            title=data.get('title'),
            description=data.get('description')

        )
        new_recipe.save()
        return new_recipe, 201


@api.route('/recipe/<int:id>')
class RecipeResource(Resource):

    @api.marshal_with(recipe_model)
    def get(self, id):
        """Get a recipe by id"""
        recipe=Recipe.query.get_or_404(id)

        return recipe

    @api.marshal_with(recipe_model)
    def patch(self, id):
        """Update a recipe by id"""
        recipe_to_update=Recipe.query.get_or_404(id)

        data=request.get_json()
        recipe_to_update.update(data.get('title'), data.get('description'))
        return recipe_to_update

    @api.marshal_with(recipe_model)
    def delete(self, id):
        """Delete a recipe by id"""
        recipe_to_delete=Recipe.query.get_or_404(id)

        recipe_to_delete.delete()
        return recipe_to_delete


@app.shell_context_processor
def make_shell_context():
    return {
        "db":db,
        "Recipe":Recipe
    }



if __name__ == '__main__':
    app.run()