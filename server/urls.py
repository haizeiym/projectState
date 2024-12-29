from django.contrib import admin
from django.urls import path
from server.api.Node import Node
from server.api.Project import Project

urlpatterns = [
    path("admin/", admin.site.urls),
    # Node API endpoints
    path("api/node/create", Node.create, name="node_create"),
    path("api/node/delete/<int:node_id>", Node.delete, name="node_delete"),
    path("api/node/update/<int:node_id>", Node.update, name="node_update"),
    path("api/node/get/<int:node_id>", Node.get, name="node_get"),
    # path("api/node/list", Node.list, name="node_list"),
    # Project API endpoints
    path("api/project/create", Project.create, name="project_create"),
    path("api/project/delete/<int:project_id>", Project.delete, name="project_delete"),
    path("api/project/update/<int:project_id>", Project.update, name="project_update"),
    path("api/project/get/<int:project_id>", Project.get, name="project_get"),
    # path("api/project/list", Project.list, name="project_list"),
]
