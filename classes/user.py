
class User:

    def __init__(self, request, session, db):
        from models import System_message
        from models import User
        from consts import severity

        path = request.path.split('/')
        self.path = path[len(path)-1]

        if 'user_id' in session:
            self.logged_in = True
            self.id = session['user_id']
            self.unread_messages = db.session.query(System_message).filter(System_message.user_id == self.id).filter(System_message.read == 0) \
			.filter(System_message.severity >= severity).count()
            self.user_object = db.session.query(User).filter(User.id == self.id).first()
            self.is_admin = True if self.user_object.level > 1 else False 
        else:
            self.logged_in = False
            self.id = 0
            self.unread_messages = 0
            self.is_admin = False
        
		