from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ravelry_un = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User user_id={self.user_id} ravelry_un={self.ravelry_un}>"


class Category(db.Model):
    """Hard coded table of user pattern categories. """

    __tablename__ = "categories"

    category_code= db.Column(db.String(5), primary_key=True, unique=True)
    title = db.Column(db.String(9), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<List Code {self.list_code} is short for {self.title}>"


class Users_Categories(db.Model):
    """ Patterns in user's queue/library/favorites. """

    __tablename__ = "users_cats"

    u_c_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category_code = db.Column(db.String(5), db.ForeignKey('categories.category_code'))
    pattern_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    category = db.relationship("Category",
                            backref=db.backref("users_cats"))

    user = db.relationship("User", 
                            backref=db.backref("users_cats"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<u_c_id={self.u_c_id} category_code={self.list_code} pattern_id={self.pattern_id} user_id={self.user_id}>"


class Projects(db.Model):

    __tablename__ = "projects"

    project_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    rav_project_id = db.Column(db.Integer, nullable=False)
    pattern_id = db.Column(db.Integer, nullable=False) #skip projects that don't have patterns since we can't get patt_type
    pattern_type = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<project_id={self.project_id} user_id={self.user_id} pattern_id={self.pattern_id}"


# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///patterns'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app

    connect_to_db(app)
    print("Connected to DB.")