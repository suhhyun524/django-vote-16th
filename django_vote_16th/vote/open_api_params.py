from drf_yasg import openapi


demo_vote = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'team': openapi.Schema(type=openapi.TYPE_STRING, description='vote for'),
    }
)

part_get = [
    openapi.Parameter(
        "part",
        openapi.IN_QUERY,
        description="front or back",
        type=openapi.TYPE_STRING,
    )
]

part_vote = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='vote for'),
    }
)
