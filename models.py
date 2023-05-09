from exts import db


"""
class Recipe:
    id: int primary key
    title: str
    description: str (text)

"""

class Recipe(db.Model):
    __tablename__ = 'recipes'
    id=db.Column(db.Integer(), primary_key=True)
    title=db.Column(db.String(), nullable=False)
    description=db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f"<Recipe {self.title}"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, title, description):
        self.title=title
        self.description=description

        db.session.commit()

class User(db.Model):
    # __tablename__ = 'users'
    id=db.Column(db.Integer(), primary_key=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(80), unique=True, nullable=False)
    password=db.Column(db.String(120), nullable=False)


    def __repr__(self):
        return f"<User {self.username}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, title, description):
        self.title=title
        self.description=description

        db.session.commit()

    def to_dict(self):
        return {
            'id':self.id,
            'username': self.username,
            'email': self.email,
            'password':self.password
        }
