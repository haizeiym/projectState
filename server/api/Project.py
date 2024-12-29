from ..models import ProjectModel
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import JsonResponse


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
            project = ProjectModel.objects.get(project_id=project_id)
            return project
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
    def create(**kwargs):
        """
        创建项目
        :param kwargs: 项目参数
        :return: Project对象或None
        """
        with transaction.atomic():
            try:
                project_id = ProjectModel.get_next_id() or 1

                project_model = ProjectModel(
                    project_id=project_id,
                    project_name=kwargs.get("project_name"),
                    description=kwargs.get("description"),
                    state=kwargs.get("state", 0),
                    node_id=kwargs.get("node_id"),
                )
                project_model.save()
                project_model.project_id = project_id
                return Project.create_from_db(project_model)
            except Exception:
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
        if project_model is None:
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

    @staticmethod
    def list(request):
        if request.method == "GET":
            try:
                projects = Project.objects.all()
                response_data = []

                for project in projects:
                    project_data = {
                        "id": project.id,
                        "name": project.name,
                        # 根据您的Project模型添加其他需要的字段
                    }
                    response_data.append(project_data)

                return JsonResponse(response_data, safe=False)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

        return JsonResponse({"error": "Invalid request method"}, status=405)
