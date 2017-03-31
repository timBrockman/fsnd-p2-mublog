"""
start models
extend db.Model
  PostEntity
  AuthorEntity
  LikeEntity
  CommentEntity
"""
from google.appengine.ext import db


class PostEntity(db.Model):
    """ db blog post entity
        properties
            subject: blog post title
            content: blog post body
            created: timestamp in normal y-m-d h:m:s
            author: author username
            likes: number of likes
    """
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(required=True)
    author = db.StringProperty(required=True)
    like_total = db.IntegerProperty(required=True)
    # liked_by = db.StringListProperty(required=True) # could be child entity


class AuthorEntity(db.Model):
    """ db author entity
        properties
            username: unique string
            username_lc: unique string lowercase version of username
            password: hashed pass + SECRET + salt
            email: optional email address
    """
    username = db.StringProperty(required=True)
    username_lc = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty()

class LikeEntity(db.Model):
    """ like entity keeps track of individual likes
        ReferenceProperty for PostEntity
        Must have AuthorEntity id and username as well
        properties
            parent = PostEntity id
    """
    for_post = db.ReferenceProperty(PostEntity, collection_name="likes")
    author = db.ReferenceProperty(AuthorEntity, collection_name="likes")
    author_username = db.StringProperty(required=True) # for quick reference only


class CommentEntity(db.Model):
    """ db comments
        properties
    """
    coment_text = db.TextProperty(required=True)
    for_post = db.ReferenceProperty(PostEntity, collection_name="comments")
    author = db.ReferenceProperty(AuthorEntity, collection_name="comments")
    author_username = db.StringProperty(required=True) # for quick reference only

