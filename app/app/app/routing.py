from django.urls import path, re_path, include
import live_logger.routing as live_logger_routing

websocket_urlpatterns = [] + live_logger_routing.websocket_urlpatterns