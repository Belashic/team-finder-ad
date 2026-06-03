from django import forms

from team_finder.utils import validate_github_url

from projects.models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'github_url', 'status']
        labels = {
            'name': 'Название проекта',
            'description': 'Описание проекта',
            'github_url': 'Ссылка на GitHub',
            'status': 'Статус',
        }

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url', '')
        return validate_github_url(url)