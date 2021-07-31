from django.db import models
from colorfield.fields import ColorField
from users.models import CustomUser


class Follow(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='Пользователь подписчик')
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Пользователь на которого подписываемся')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ['author', 'user']

    def __str__(self):
        return f'{self.user} => {self.author}'


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        help_text='Введите название тега',
        max_length=200,
        unique=True,
    )
    color = ColorField(
        verbose_name='Цвет в HEX',
        help_text='Введите цвет тега в HEX',
        unique=True,
        null=True,
    )
    slug = models.CharField(
        verbose_name='Уникальный слаг',
        help_text='Введите уникальный слаг',
        max_length=200,
        unique=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):

    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
        help_text='Введите название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=20,
        verbose_name='Единица измерения',
        help_text='Выберите единицу измерения'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT,
        related_name='recipes', verbose_name='Автор рецепта'
    )
    title = models.CharField(
        max_length=50, verbose_name='Название рецепта'
    )
    image = models.ImageField(
        verbose_name='Картинка',
        help_text='Выберите изображение'
    )
    description = models.TextField(
        max_length=1000, verbose_name='Описание рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientForRecipe',
        verbose_name='Ингредиенты',
        help_text='Укажите ингредиенты и их количество'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления'
    )
    tag = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        help_text='Выберите один или несколько тегов'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title


class IngredientForRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        null=True,
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Количество ингредиента в рецепте'

    def __str__(self):
        return f'{self.ingredient} в {self.recipe}'

