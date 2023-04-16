from django.urls import path
from .views import RegisterView, LoginView, ProfileView, RecordCollectionView, RecordWishlistView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('<int:id>/', ProfileView.as_view()),
    path('<int:id1>/collection/<int:id2>/', RecordCollectionView.as_view()),
    path('<int:id1>/wishlist/<int:id2>/', RecordWishlistView.as_view())
]