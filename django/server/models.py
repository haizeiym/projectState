from django.db import models
from django.db import transaction
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


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

    def sync_state_from_node(self):
        """从关联节点同步状态"""
        if self.node_id:
            try:
                node = NodeModel.objects.get(node_id=self.node_id)
                if self.state != node.state:
                    self.state = node.state
                    self.save()
            except NodeModel.DoesNotExist:
                pass

    def save(self, *args, **kwargs):
        """重写保存方法，在保存时同步节点状态"""
        if not self.pk:  # 新建项目时
            super().save(*args, **kwargs)
            self.sync_state_from_node()
        else:  # 更新项目时
            super().save(*args, **kwargs)


@receiver(post_save, sender=NodeModel)
def sync_project_states(sender, instance, **kwargs):
    """
    当节点保存时，同步关联项目的状态
    """
    from .models import ProjectModel  # 避免循环导入

    # 确保 node_id 是整数类型
    try:
        node_id = int(instance.node_id)
    except (TypeError, ValueError):
        print(f"Warning: Invalid node_id type: {type(instance.node_id)}")
        return

    # 查找关联到此节点的所有项目
    projects = ProjectModel.objects.filter(node_id=node_id)
    for project in projects:
        project.sync_state_from_node()


class PNTGModel(models.Model):
    project_id = models.IntegerField(
        primary_key=True,
        validators=[MinValueValidator(0)],
        verbose_name="项目ID",
        help_text="项目的ID",
    )

    state_codes = models.TextField(
        verbose_name="状态码",
        help_text="状态码",
    )

    bot_token = models.CharField(
        max_length=255,
        verbose_name="Telegram Bot Token",
        help_text="Telegram Bot Token",
    )

    chat_id = models.CharField(
        max_length=255,
        verbose_name="Telegram Chat ID",
        help_text="Telegram Chat ID",
    )

    url = models.TextField(
        verbose_name="Telegram URL",
        help_text="Telegram URL",
    )

    class Meta:
        db_table = "pntg"
        verbose_name = "PNTG"
        verbose_name_plural = "PNTG"
        ordering = ["project_id"]


class StateCodeModel(models.Model):
    state_code = models.IntegerField(
        primary_key=True,
        verbose_name="状态码",
        help_text="状态码",
    )

    state_name = models.CharField(
        max_length=255,
        verbose_name="状态名称",
        help_text="状态名称",
    )

    class Meta:
        db_table = "state_code"
        verbose_name = "状态码"
        verbose_name_plural = "状态码"
        ordering = ["state_code"]
