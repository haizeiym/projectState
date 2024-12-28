from djongo import models


class NodeModel(models.Model):
    parent_id = models.IntegerField(default=0)
    node_id = models.IntegerField(primary_key=True)
    state = models.IntegerField(default=0)
    node_name = models.CharField(max_length=255, default="")
    description = models.TextField(default="")
    children_state = models.IntegerField(default=0)

    class Meta:
        db_table = "nodes"


class ProjectModel(models.Model):
    project_id = models.IntegerField(primary_key=True)
    project_name = models.CharField(max_length=100)
    description = models.TextField(default="")
    state = models.IntegerField(default=0)
    node_id = models.IntegerField(default=0)

    class Meta:
        db_table = "projects"
