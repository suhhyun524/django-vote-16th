from drf_yasg import openapi

get_params = [
    openapi.Parameter(
        "part",
        openapi.IN_QUERY,
        description="front or back",
        type=openapi.TYPE_STRING,
    )
]


post_params = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='vote for'),
    }
)
