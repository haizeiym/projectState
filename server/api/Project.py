from ..model.models import ProjectModel
from django.core.exceptions import ObjectDoesNotExist


class Project:
    def __init__(self, project_id, project_name="", description="", state=0, node_id=0):
        self.project_id = project_id
        self.project_name = project_name
        self.description = description
        self.state = state
        self.node_id = node_id

    @staticmethod
    def _get_project_model(project_id):
        """
        获取项目模型的辅助方法
        :param project_id: 项目ID
        :return: ProjectModel实例或None
        """
        try:
            return ProjectModel.objects.filter(project_id=project_id).first()
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get(project_id):
        """
        获取项目信息
        :param project_id: 项目ID
        :return: Project对象或None
        """
        project_model = Project._get_project_model(project_id)
        return Project.create_from_db(project_model)

    @staticmethod
    def create(project_id, project_name, description="", state=0, node_id=0):
        """
        创建或更新项目
        :param project_id: 项目ID
        :param project_name: 项目名称
        :param description: 项目描述
        :param state: 项目状态
        :param node_id: 项目节点ID
        :return: Project对象或None
        """
        try:
            project, created = ProjectModel.objects.update_or_create(
                project_id=project_id,  # 查询条件
                defaults={  # 需要更新或创建的字段
                    "project_name": project_name,
                    "description": description,
                    "state": state,
                    "node_id": node_id,
                },
            )
            return Project.create_from_db(project)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def update(project_id, **kwargs):
        """
        更新项目信息
        :param project_id: 项目ID
        :param kwargs: 要更新的字段和值
        :return: 是否更新成功
        """
        project_model = Project._get_project_model(project_id)
        if not project_model:
            return False

        field_mapping = {
            "project_name": "project_name",
            "description": "description",
            "state": "state",
            "node_id": "node_id",
        }

        try:
            for key, value in kwargs.items():
                if key in field_mapping:
                    setattr(project_model, field_mapping[key], value)
            project_model.save()
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def delete(project_id):
        """
        删除项目
        :param project_id: 项目ID
        :return: 是否删除成功
        """
        project_model = Project._get_project_model(project_id)
        if not project_model:
            return False
        try:
            project_model.delete()
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def create_from_db(project_model):
        """
        从数据库模型创建Project对象
        :param project_model: ProjectModel实例
        :return: Project对象
        """
        if not project_model:
            return None

        return Project(
            project_id=project_model.project_id,
            project_name=project_model.project_name,
            description=project_model.description,
            state=project_model.state,
            node_id=project_model.node_id,
        )
