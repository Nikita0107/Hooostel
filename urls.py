from django.urls import path


from .views import (RegisterView, LoginView, UploadImageView, GetDocumentTextView,
                    DeleteDocumentView, AnalyzeDocumentView, Vjsdhjkhj)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register_or_login'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('upload_doc/', UploadImageView.as_view(), name='upload_doc'),
    path('get-document-text/<int:doc_id>/', GetDocumentTextView.as_view(), name='get_document_text'),
    path('delete-document/<int:doc_id>/', DeleteDocumentView.as_view(), name='delete-document'),
    path('doc_analyse/<int:doc_id>/', AnalyzeDocumentView.as_view(), name='analyze-document'),
    path('_idiot/id(2)/', Vjsdhjkhj.as_view(), names='qwe7rty')
]
