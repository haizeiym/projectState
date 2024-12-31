from django.db import models
from django.db import transaction
from django.core.validators import MinValueValidator


class NodeModel(models.Model):
    """节点模型
    用于存储节点的基本信息和树形结构
    """

    # 基本信息字段
    node_id = models.AutoField(
        primary_key=True, verbose_name="节点ID", help_text="节点的唯一标识符"
    )
    node_name = models.CharField(
        max_length=255, verbose_name="节点名称", help_text="节点的显示名称"
    )
    description = models.TextField(
        null=True, blank=True, verbose_name="描述", help_text="节点的详细描述"
    )

    # 状态字段
    state = models.IntegerField(
        default=0,
        verbose_name="状态",
        help_text="节点的当前状态",
    )

    # 树形结构字段
    parent_id = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="父节点ID",
        help_text="父节点的ID，0表示根节点",
    )

    class Meta:
        db_table = "node"
        verbose_name = "节点"
        verbose_name_plural = "节点"
        ordering = ["node_id"]
        indexes = [models.Index(fields=["parent_id"]), models.Index(fields=["state"])]

    def __str__(self):
        return f"{self.node_name}(ID:{self.node_id})"

    @classmethod
    def get_next_id(cls):
        """获取下一个节点ID
        使用事务确保唯一性

        Returns:
            int: 下一个可用的节点ID
        """
        with transaction.atomic():
            max_id = cls.objects.aggregate(max_id=models.Max("node_id"))["max_id"]
            return (max_id or 100000000) + 1

    def get_childrens(self):
        """获取子节点ID列表

        Returns:
            list: 子节点ID列表
        """
        return list(
            NodeModel.objects.filter(parent_id=self.node_id).values_list(
                "node_id", flat=True
            )
        )

    def add_child(self, child_id):
        """添加子节点

        Args:
            child_id (int): 要添加的子节点ID
        """
        child_node = NodeModel.objects.filter(node_id=child_id).first()
        if child_node and child_node.parent_id != self.node_id:
            child_node.parent_id = self.node_id
            child_node.save()

    def remove_child(self, child_id):
        """移除子节点

        Args:
            child_id (int): 要移除的子节点ID
        """
        child_node = NodeModel.objects.filter(
            node_id=child_id, parent_id=self.node_id
        ).first()
        if child_node:
            child_node.parent_id = 0
            child_node.save()


class ProjectModel(models.Model):
    """项目模型
    用于存储项目的基本信息和关联节点
    """

    # 基本信息字段
    project_id = models.AutoField(
        primary_key=True, verbose_name="项目ID", help_text="项目的唯一标识符"
    )
    project_name = models.CharField(
        max_length=255, verbose_name="项目名称", help_text="项目的显示名称"
    )
    description = models.TextField(
        null=True, blank=True, verbose_name="描述", help_text="项目的详细描述"
    )

    # 状态字段
    state = models.IntegerField(
        default=0,
        verbose_name="状态",
        help_text="项目的当前状态",
    )

    # 关联节点
    node_id = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="关联节点ID",
        help_text="项目关联的主节点ID",
    )

    class Meta:
        db_table = "project"
        verbose_name = "项目"
        verbose_name_plural = "项目"
        ordering = ["project_id"]
        indexes = [
            models.Index(fields=["node_id"]),
            models.Index(fields=["state"]),
        ]

    def __str__(self):
        return f"{self.project_name}(ID:{self.project_id})"

    @classmethod
    def get_next_id(cls):
        """获取下一个项目ID
        使用事务确保唯一性

        Returns:
            int: 下一个可用的项目ID
        """
        with transaction.atomic():
            max_id = cls.objects.aggregate(max_id=models.Max("project_id"))["max_id"]
            return (max_id or 100000000) + 1

    def get_node(self):
        """获取关联的节点对象

        Returns:
            NodeModel: 关联的节点对象，如果不存在返回None
        """
        if self.node_id:
            return NodeModel.objects.filter(node_id=self.node_id).first()
        return None

    def set_node(self, node_id):
        """设置关联的节点ID

        Args:
            node_id (int): 要关联的节点ID
        """
        self.node_id = node_id
