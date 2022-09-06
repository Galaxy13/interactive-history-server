from fastapi import FastAPI, HTTPException, Body, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from models import *
from typing import List, Optional
import mongodb

app = FastAPI()
db = mongodb.MongoConnection()


@app.get('/', response_description='Welcome Phrase')
async def root():
    return 'Welcome to Interactive History Project!'


@app.get('/api/v1/classes', response_description="List all classes", response_model=List[Class])
async def get_all_classes():
    if (classes := db.db.classes.find()) is not None:
        return [new_class for new_class in classes]
    raise HTTPException(status_code=400, detail='No classes added')


@app.get('/api/v1/classes/{class_id}', response_description='List all class lessons', response_model=List[Lesson])
async def get_class_lessons(class_id: str):
    if db.find_class_by_id(class_id) is not None:
        if (lessons := db.get_class_lessons(class_id)) is not None:
            return [lesson for lesson in lessons]
        raise HTTPException(status_code=404, detail=f'No lessons in {class_id}')
    raise HTTPException(status_code=404, detail=f'No class with id {class_id} existing')


@app.get('/api/v1/lessons/{lesson_id}', response_description='Open first slide', response_model=List)
async def open_lesson(lesson_id: str):
    if db.find_lesson_by_id(lesson_id):
        if (slide := db.open_lesson_slide(lesson_id)) is not None:
            return jsonable_encoder(slide['objects'])

        raise HTTPException(status_code=404, detail=f'No slides in {lesson_id}')
    raise HTTPException(status_code=404, detail=f'No lesson with id {lesson_id} existing')


@app.post('/api/v1/classes', response_description='Add new class', response_model=Class)
async def create_class(class_obj: Class = Body(...)):
    class_obj = jsonable_encoder(class_obj)
    new_class = db.create_class(class_obj)
    created_class = db.show_created_class(new_class)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_class)


@app.post('/api/v1/classes/{class_id}', response_description='Create new lesson in class', response_model=Lesson)
async def create_lesson(class_id, lesson_obj: Lesson = Body(...)):
    if db.find_class_by_id(class_id):
        lesson_obj = jsonable_encoder(lesson_obj)
        lesson_obj['class_id'] = class_id
        new_lesson = db.create_lesson(lesson_obj)
        created_lesson = db.show_created_lesson(new_lesson)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_lesson)
    raise HTTPException(status_code=404, detail=f'Class with id: {class_id} is not existing')

@app.post('/api/v1/lessons/{lesson_id}', response_description='Create new slide', response_model=Slide)
async def create_slide(lesson_id, slide_obj: Slide = Body(...)):
    if db.find_lesson_by_id(lesson_id) is not None:
        slide_obj = jsonable_encoder(slide_obj)
        slide_obj['lesson_id'] = lesson_id
        new_slide = db.create_new_slide(slide_obj)
        created_slide = db.show_created_slide(new_slide)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_slide)
    raise HTTPException(status_code=404, detail=f'No lesson with id {lesson_id} existing')
