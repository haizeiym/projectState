from django.db import models
from django.db import transaction
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from djongo import models as djongo_models
from bson import ObjectId
from djongo.models import ObjectIdField


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
    project_id = models.IntegerField(primary_key=True)
    project_name = models.CharField(max_length=255)
    description = models.TextField()

    # 状态字段
    state = models.IntegerField(default=0)

    # 关联节点
    node_id = models.IntegerField(default=0)

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
    _id = ObjectIdField(primary_key=True, default=ObjectId)
    tg_id = models.IntegerField(
        unique=True,
        validators=[MinValueValidator(1000)],
        verbose_name="Telegram ID",
        help_text="Telegram 配置的唯一标识符",
    )

    tg_name = models.CharField(
        max_length=255,
        verbose_name="Telegram 名称",
        help_text="Telegram 配置的名称",
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

    state_code = models.TextField(
        default="0",
        verbose_name="状态码",
        help_text="状态码",
    )

    class Meta:
        db_table = "pntg"
        verbose_name = "PNTG"
        verbose_name_plural = "PNTG"
        ordering = ["tg_id"]

    def save(self, *args, **kwargs):
        # 如果没有 tg_id，获取当前最大值并加1
        if not self.tg_id:
            try:
                max_tg_id = PNTGModel.objects.aggregate(max_id=models.Max("tg_id"))[
                    "max_id"
                ]
                self.tg_id = (max_tg_id or 999) + 1
            except Exception:
                self.tg_id = 1000
        super().save(*args, **kwargs)


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


class UMModel(AbstractUser):
    # MongoDB 的 ObjectId
    _id = djongo_models.ObjectIdField(default=ObjectId)

    # 使用 IntegerField 而不是 AutoField
    user_id = models.IntegerField(
        unique=True,
        null=True,
        blank=True,
        verbose_name="用户ID",
        help_text="用户的整数ID",
    )

    project_ids = models.TextField(
        verbose_name="项目IDs",
        help_text="关联的项目ID列表，用逗号分隔",
        blank=True,
        default="",
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    class Meta:
        db_table = "auth_user"
        verbose_name = "用户"
        verbose_name_plural = "用户"

    def save(self, *args, **kwargs):
        # 如果没有设置 user_id，则生成一个新的
        if not self.user_id:
            # 获取当前最大的 user_id
            max_id = UMModel.objects.all().aggregate(models.Max("user_id"))[
                "user_id__max"
            ]
            self.user_id = (max_id or 100000) + 1
        super().save(*args, **kwargs)

    @property
    def id(self):
        """
        为了兼容性，返回用户ID
        """
        return self.user_id or self.pk

    def get_project_ids(self):
        """将字符串形式的项目ID转换为列表"""
        return [int(pid) for pid in self.project_ids.split(",") if pid]

    def add_project_id(self, project_id):
        """添加项目ID"""
        current_ids = self.get_project_ids()
        if project_id not in current_ids:
            current_ids.append(project_id)
            self.project_ids = ",".join(map(str, current_ids))
            self.save()

    def remove_project_id(self, project_id):
        """移除项目ID"""
        current_ids = self.get_project_ids()
        if project_id in current_ids:
            current_ids.remove(project_id)
            self.project_ids = ",".join(map(str, current_ids))
            self.save()

    def has_project_access(self, project_id):
        """检查用户是否有权限访问特定项目"""
        return project_id in self.get_project_ids()
