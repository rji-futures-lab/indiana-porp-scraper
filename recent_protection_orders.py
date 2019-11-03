import os
from models import RestrainingOrder


cached_ids = [
    i.strip('.html') for i in os.listdir('.cache/SearchDetail/')
    if i.endswith('.html')
]

query = (
    RestrainingOrder
        .select(RestrainingOrder.id)
        .where(
            (
                RestrainingOrder.date_filed.endswith('2017') | 
                RestrainingOrder.date_filed.endswith('2018') | 
                RestrainingOrder.date_filed.endswith('2019')
            ) & (
                RestrainingOrder.case_number.contains('PO') 
            ) & ( 
                RestrainingOrder.id.not_in(cached_ids)
            )
        )
        .order_by(RestrainingOrder.id)
)
