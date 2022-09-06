from pymongo import MongoClient
import secret

class MongoConnection:
    def __init__(self, host='mongodb',
                 login=secret.LOGIN,
                 passwd=secret.PASSWD,
                 port='27017', db_name='test'):
        self.client = MongoClient(f'mongodb://{login}:{passwd}@{host}:{port}')
        self.db = self.client[db_name]

    def get_all_classes(self):
        classes = self.db.classes.find({})
        for class_obj in classes:
            class_obj['id'] = str(class_obj['_id'])
            del [class_obj['_id']]
        return {'classes': [class_obj for class_obj in classes]}

    def get_class_lessons(self, class_id):
        return self.db.lessons.find({'class_id': class_id})

    def open_lesson_slide(self, lesson_id, slide_number=1):
        return self.db.slides.find_one({'lesson_id': lesson_id,
                                        'slide_number': slide_number})

    def create_class(self, class_obj):
        return self.db.classes.insert_one(class_obj)

    def show_created_class(self, class_obj):
        return self.db.classes.find_one({'_id': class_obj.inserted_id})

    def create_lesson(self, lesson_obj):
        return self.db.lessons.insert_one(lesson_obj)

    def show_created_lesson(self, lesson_obj):
        return self.db.lessons.find_one({'_id': lesson_obj.inserted_id})

    def find_class_by_id(self, class_id):
        return self.db.classes.find_one({'_id': class_id})

    def find_lesson_by_id(self, lesson_id):
        return self.db.lessons.find_one({'_id': lesson_id})

    def create_new_slide(self, slide_obj):
        return self.db.slides.insert_one(slide_obj)

    def show_created_slide(self, slide_obj):
        return self.db.slides.find_one({'_id': slide_obj.inserted_id})
