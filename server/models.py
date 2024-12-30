from django.db import models, transaction
from django.db.models import F
from djongo import models as djongo_models


class NodeModel(models.Model):
    node_id = models.AutoField(primary_key=True)
    node_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    state = models.IntegerField(default=0)
    parent_id = models.IntegerField(default=0)
    children_state = models.IntegerField(default=0)
    childrens = models.TextField(default="")

    class Meta:
        db_table = "node"

    @classmethod
    def get_next_id(cls):
        """
        获取下一个节点ID,使用事务确保唯一性
        """
        with transaction.atomic():
            max_id = cls.objects.aggregate(max_id=models.Max("node_id"))["max_id"]
            next_id = (max_id or 100000000) + 1
            return next_id

    def get_childrens(self):
        """获取子节点 ID 列表"""
        return (
            [int(x) for x in self.childrens.split(",") if x] if self.childrens else []
        )

    def set_childrens(self, ids):
        """设置子节点 ID 列表"""
        self.childrens = ",".join(str(x) for x in ids)


class ProjectModel(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    state = models.IntegerField(default=0)
    node_id = models.IntegerField(default=0)

    class Meta:
        db_table = "project"

    @classmethod
    def get_next_id(cls):
        """
        获取下一个项目ID,使用事务确保唯一性
        """
        with transaction.atomic():
            # 直接使用 aggregate 获取最大 ID，减少数据库查询
            max_id = cls.objects.aggregate(max_id=models.Max("project_id"))["max_id"]
            next_id = (max_id or 100000000) + 1
            return next_id
