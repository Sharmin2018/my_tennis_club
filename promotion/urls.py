from django.urls import path
from .views import PromotionView
from .views import PromotionHistoryView

urlpatterns = [

    path(
        "",
        PromotionView.as_view(),
        name="promotion",
    ),

    path(
    "history/",
    PromotionHistoryView.as_view(),
    name="promotion_history",
),

]