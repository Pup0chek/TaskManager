from fastapi import APIRouter

router = APIRouter(prefix='/items', tags=['Items'])





@router.get('/')
def get_items():
    return [
        "Item1",
        "Item2",
        "Item3"
    ]
#от частного к общему, порядок важен
@router.get('/latest')
def get_lates():
    return {"item":{
        'id': 0,
        'name': "prikol"
    }}

@router.get('/{item_id}')
def get_item(item_id: int):
    return {"id": item_id}