from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='pokemon_images', blank=True, null=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemons = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(blank=True, null=True)
    disappeared_at = models.DateTimeField(blank=True, null=True)
    level = models.IntegerField(default=0)
    health = models.IntegerField(default=0)
    strength = models.IntegerField(default=0)
    defence = models.IntegerField(default=0)
    stamina = models.IntegerField(default=0)
