from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import (SyncUserView, LoginView, UploadImageView, GetDocumentTextView,
                    DeleteDocumentView, AnalyzeDocumentView)


urlpatterns = [
    path('SyncUser/', SyncUserView.as_view(), name='SyncUsers'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('get-document-text/<int:doc_id>/', GetDocumentTextView.as_view(), name='get-document-text'),
    path('upload_doc/', UploadImageView.as_view(), name='upload_doc'),
    path('delete-document/<int:doc_id>/', DeleteDocumentView.as_view(), name='delete-document'),
    path('doc_analyse/<int:doc_id>/', AnalyzeDocumentView.as_view(), name='analyze-document'),
]
