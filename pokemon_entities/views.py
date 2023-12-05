import folium
from django.utils.timezone import localtime
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404

from pokemon_entities.models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    time = localtime()

    for pokemon_entity in PokemonEntity.objects.filter(disappeared_at__gte=time, appeared_at__lte=time).all():
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemons.image.url)
        )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url if pokemon.image else DEFAULT_IMAGE_URL,
            'title_ru': pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    time = localtime()

    pokemons_entity = pokemon.entities.filter(disappeared_at__gte=time, appeared_at__lte=time).all()
    img_url = request.build_absolute_uri(pokemon.image.url)

    for pokemon_entity in pokemons_entity:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            img_url
        )

    pokemon_data = {
        'pokemon_id': pokemon.id,
        'img_url': pokemon.image.url if pokemon.image else DEFAULT_IMAGE_URL,
        'title_ru': pokemon.title_ru,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description
    }

    if pokemon.previous_evolution:
        pokemon_data['previous_evolution'] = {
            'pokemon_id': pokemon.previous_evolution.id,
            'img_url': request.build_absolute_uri(pokemon.previous_evolution.image.url),
            'title_ru': pokemon.previous_evolution.title_ru
        }
    next_evolution = pokemon.next_evolutions.first()
    if next_evolution:
        pokemon_data['next_evolution'] = {
            'pokemon_id': next_evolution.id,
            'img_url': request.build_absolute_uri(next_evolution.image.url),
            'title_ru': next_evolution.title_ru
        }

    return render(
        request,
        'pokemon.html',
        context={
            'map': folium_map._repr_html_(),
            'pokemon': pokemon_data
        }
    )
