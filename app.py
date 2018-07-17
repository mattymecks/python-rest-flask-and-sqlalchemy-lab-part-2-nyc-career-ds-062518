# imported Flask and jsonify from flask
# imported SQLAlchemy from flask_sqlalchemy
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# initialized new flask app
app = Flask(__name__)
# added configurations and database
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# connected flask_sqlalchemy to the configured flask app
db = SQLAlchemy(app)

# created models for application
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    tweets = db.relationship('Tweet', backref='users', lazy=True)
    def to_dict(self):
        user = {'id': self.id, 'username': self.username, 'tweets': [tweet.to_dict() for tweet in self.tweets]}
        return user

class Tweet(db.Model):
    __tablename__ = 'tweets'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates="tweets")
    def to_dict(self):
        tweet = {'id': self.id, 'text': self.text, 'user_id': self.user.id, 'user': self.user.username}
        return tweet


# DEFINE ROUTES THAT RETURN APPROPRIATE HTML TEMPLATES HERE


#User Routes

@app.route('/users')
def users():
    user_list = User.query.all()
    return render_template('users.html', user_list=user_list)


@app.route('/users/<int:id>')
def users_by_id(id):
    user = User.query.get(id)
    tweets = user.to_dict()['tweets']
    return render_template('user_show.html', user=user, tweets=tweets)

#possible that this doesn't work
@app.route('/users/<username>')
def users_by_username(username):
    user = User.query.filter(User.username.ilike(username)).first()
    tweets = user.to_dict()['tweets']
    return render_template('user_show.html', user=user, tweets=tweets)

# Tweet Routes

@app.route('/tweets')
def tweets():
    tweet_list = Tweet.query.all()
    return render_template('tweets.html', tweet_list=tweet_list)

@app.route('/tweets/<int:id>')
def tweets_by_id(id):
    tweet = Tweet.query.get(id)
    return render_template('tweet_show.html', tweet=tweet)


#NOT YET OPTIMIZED FOR THIS LAB

# Nested Routes

@app.route('/users/<int:id>/tweets')
def tweets_by_user_id(id):
    tweet_list = Tweet.query.filter(Tweet.user_id == id).all()
    return render_template('tweets.html', tweet_list=tweet_list)

@app.route('/users/<username>/tweets')
def tweets_by_username(username):
    user = User.query.filter(User.username.ilike(username)).first()
    tweet_list = Tweet.query.filter(Tweet.user_id == user.id).all()
    return render_template('tweets.html', tweet_list=tweet_list)

@app.route('/tweets/<int:id>/user')
def user_by_tweet_id(id):
    tweet_key = Tweet.query.get(id)
    user = [user for user in User.query.all() if tweet_key in user.tweets]
    tweets = user[0].tweets
    return render_template('user_show.html', user=user[0], tweets=tweets)


# run flask application
if __name__ == "__main__":
    app.run()
