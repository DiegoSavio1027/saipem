from django.urls import path
from hse_module.hse_pob.views import (
    api_offshore_vessels,
    api_offshore_vessel_detail,
    api_offshore_locations,
    api_offshore_location_detail,
    api_assign_decks_to_vessel,
    api_unassign_deck_from_vessel
)

urlpatterns = [
    # Vessels
    path('vessels/', api_offshore_vessels, name='api_offshore_vessels'),
    path('vessels/<int:vessel_id>/', api_offshore_vessel_detail, name='api_offshore_vessel_detail'),
    path('vessels/<str:vessel_id>/assign-decks/', api_assign_decks_to_vessel, name='api_assign_decks_to_vessel'),
    path('vessels/<str:vessel_id>/assign-decks/<int:deck_id>/', api_unassign_deck_from_vessel, name='api_unassign_deck_from_vessel'),

    # Locations/Decks
    path('locations/', api_offshore_locations, name='api_offshore_locations'),
    path('locations/<int:pk>/', api_offshore_location_detail, name='api_offshore_location_detail'),
]
