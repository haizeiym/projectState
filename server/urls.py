from django.contrib import admin
from django.urls import path
from server.api.Node import Node
from server.api.Project import Project
from server.api.PNTG import PNTG
from server.api.StateCode import StateCode

urlpatterns = [
    path("admin/", admin.site.urls),
    # Node API endpoints
    path("api/node/create", Node.create, name="node_create"),
    path("api/node/delete/<int:node_id>", Node.delete, name="node_delete"),
    path("api/node/update/<int:node_id>", Node.update, name="node_update"),
    path("api/node/get/<int:node_id>", Node.get, name="node_get"),
    path("api/node/tree/<int:node_id>", Node.get_tree, name="node_tree"),
    path("api/node/batch_update", Node.batch_update, name="node_batch_update"),
    # Project API endpoints
    path("api/project/create", Project.create, name="project_create"),
    path("api/project/delete/<int:project_id>", Project.delete, name="project_delete"),
    path("api/project/update/<int:project_id>", Project.update, name="project_update"),
    path("api/project/get/<int:project_id>", Project.get, name="project_get"),
    path("api/project/list", Project.list, name="project_list"),
    # PNTG API endpoints
    path("api/pntg/create", PNTG.create, name="pntg_create"),
    path("api/pntg/delete/<int:project_id>", PNTG.delete, name="pntg_delete"),
    path("api/pntg/update/<int:project_id>", PNTG.update, name="pntg_update"),
    path("api/pntg/get/<int:project_id>", PNTG.get, name="pntg_get"),
    # StateCode API endpoints
    path("api/statecode/create", StateCode.create, name="statecode_create"),
    path(
        "api/statecode/delete/<int:state_code>",
        StateCode.delete,
        name="statecode_delete",
    ),
    path(
        "api/statecode/update/<int:state_code>",
        StateCode.update,
        name="statecode_update",
    ),
    path("api/statecode/get/<int:state_code>", StateCode.get, name="statecode_get"),
    path("api/statecode/list", StateCode.list, name="statecode_list"),
]
