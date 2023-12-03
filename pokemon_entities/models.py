from django.db import models  # noqa F401


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, verbose_name='Название на русском')
    title_en = models.CharField(max_length=200, blank=True, null=True, verbose_name='Название на английском')
    title_jp = models.CharField(max_length=200, blank=True, null=True, verbose_name='Название на японском')
    image = models.ImageField(upload_to='pokemon_images', blank=True, null=True, verbose_name='Изображение')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='next_evolution',
        verbose_name='Предыдущая эволюция'
    )

    def __str__(self):
        return self.title_ru

    class Meta:
        verbose_name = 'Вид покемона'
        verbose_name_plural = 'Виды покемонов'


class PokemonEntity(models.Model):
    pokemons = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='Покемон')
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(blank=True, null=True, verbose_name='Время появления')
    disappeared_at = models.DateTimeField(blank=True, null=True, verbose_name='Время исчезновения')
    level = models.IntegerField(default=0, verbose_name='Уровень')
    health = models.IntegerField(default=0, verbose_name='Здоровье')
    strength = models.IntegerField(default=0, verbose_name='Сила')
    defence = models.IntegerField(default=0, verbose_name='Защита')
    stamina = models.IntegerField(default=0, verbose_name='Выносливость')

    def __str__(self):
        return self.pokemons.title_ru

    class Meta:
        verbose_name = 'Покемон'
        verbose_name_plural = 'Покемоны'
