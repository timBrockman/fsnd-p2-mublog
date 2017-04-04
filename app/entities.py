"""
start models
extend db.Model
  PostEntity
  AuthorEntity
  LikeEntity
  CommentEntity
"""
from hasher import hash_this, check_hash
from google.appengine.ext import db

class AuthorEntity(db.Model):
    """ db author entity

        :param username: unique string
        :param pw_hash: hashed (pass + SECRET + salt)
        :param email: optional email address
        classmethod
            read_by_id
            read_my_name
            register (create)
            login
    """
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty()

    @classmethod
    def read_by_id(cls, uid):
        """convienient get_by_id method"""
        return AuthorEntity.get_by_id(uid)

    @classmethod
    def read_my_name(cls, username):
        """convienient filter by username method"""
        return AuthorEntity.all().filter('username =', username).get()

    @classmethod
    def register(cls, username, password, email):
        """creates new user (doesn't check if one exsist)"""
        pw_hash = hash_this(password)
        return AuthorEntity()

    @classmethod
    def login(cls, username, password):
        """logs in user if credentials check out"""
        pass

class PostEntity(db.Model):
    """ db blog post entity

        :param subject: blog post title
        :param content: blog post body
        :param created: timestamp in normal y-m-d h:m:s
        :param author: author username
        :param like_total: number of likes
        classmethod
            create
            update_by_id
            read_by_id
            delete_by_id
    """
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(required=True)
    author = db.ReferenceProperty(AuthorEntity, collection_name="blog_posts")
    like_total = db.IntegerProperty(required=True)



class LikeEntity(db.Model):
    """ like entity keeps track of individual likes

        ReferenceProperty for PostEntity
        Must have AuthorEntity id and username as well
        :param for_post = reference PostEntity
        :param author_username = AuthorEntity username
        :param author = reference AuthorEntity
    """
    for_post = db.ReferenceProperty(PostEntity, collection_name="likes")
    author = db.ReferenceProperty(AuthorEntity, collection_name="likes")
    author_username = db.StringProperty(required=True)


class CommentEntity(db.Model):
    """ db comments
        properties
    """
    coment_text = db.TextProperty(required=True)
    for_post = db.ReferenceProperty(PostEntity, collection_name="comments")
    author = db.ReferenceProperty(AuthorEntity, collection_name="comments")
    author_username = db.StringProperty(required=True) # for quick reference only

