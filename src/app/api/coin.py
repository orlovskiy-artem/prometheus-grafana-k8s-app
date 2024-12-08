import random
from fastapi import APIRouter, HTTPException, Response
import prometheus_client
from app.api import crud
from app.api.models import NoteSchema
router = APIRouter()

heads_counter = prometheus_client.Counter(
    'heads_counter',
    'The number of heads'
)
tails_counter = prometheus_client.Counter(
    'tails_counter',
    'The number of tails'
)
flip_coins_total = prometheus_client.Counter(
    'flip_coins_total',
    'The total number of coin flips'
)

@router.get("/flip-coins")
async def flip_coins(times=None):
    if times is None or not times.isdigit():
        raise HTTPException(
            status_code=400,
            detail="times must be set in request and an integer",
        )
    heads = 0
    times_as_int = int(times)
    for _ in range(times_as_int):
        # this will be 0 or 1, if 1, it evaluates to True
        if random.randint(0, 1):
            heads += 1
    tails = times_as_int - heads
    flip_coins_total.inc(times_as_int)
    heads_counter.inc(heads)
    tails_counter.inc(tails)
    await crud.post(
        NoteSchema(
            title=f"Coin flip {times_as_int}",
            description=f"Coin flip ratio {heads}/{tails}",
            completed="True"
        )
    )
    return {
        "heads": heads,
        "tails": tails
    }


@router.get("/metrics")
def get_metrics():
    return Response(
        content=prometheus_client.generate_latest(),
        media_type=prometheus_client.CONTENT_TYPE_LATEST
    )
