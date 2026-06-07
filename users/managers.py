import random
import io

from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager
from django.core.files.base import ContentFile 

from PIL import Image, ImageDraw, ImageFont

import constants


class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, phone, password=None, **extra_fields):
        if not email:
            raise ValueError('Email является обязательным полем')
        if not name or not surname:
            raise ValueError('Имя и Фамилия являются обязательными полями')
        if not phone:
            raise ValueError('Номер телефона является обязательным полем')

        email = self.normalize_email(email)
        
        extra_fields.setdefault('is_active', True)
        
        user = self.model(
            email=email,
            name=name,
            surname=surname,
            phone=phone,
            **extra_fields
        )
        
        if not user.avatar:
            
            user.avatar = generate_avatar(name[0], number_of_user=self.model.objects.count())

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff'):
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser'):
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, name, surname, phone, password, **extra_fields)


def generate_avatar(letter, number_of_user):
    is_lucky_user = random.choice([False, True]) #Если пользователь удачливый, то его фон будет в цвет Яндекса))))
    if is_lucky_user:
        r = 255
        g = 204
        b = 0
    else:
        r = random.randint(0, 110)
        g = random.randint(0, 110)
        b = random.randint(0, 110)
    background_color = (r, g, b)
    text_color = constants.TEXT_COLOR
    
    img = Image.new('RGB', (constants.IMAGE_SIZE, constants.IMAGE_SIZE), color=background_color)
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 120)
    except IOError:
        font = None
        
    letter = letter.upper()
    
    draw.text((100, 100), letter, fill=text_color, font=font, anchor="mm")
    
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue(), name=f'avatar_{number_of_user}.png')
