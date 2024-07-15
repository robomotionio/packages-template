from robomotion.node import Node
from robomotion.decorators import register_node
from robomotion.variable import InVariable, OutVariable
from robomotion.message import Context

from nodes.auth_manager import github_auth_manager
from nodes.icon import github_icon

@register_node(name='Robomotion.GitHub.Issues.GetIssue', title='Get Issue', color='#0D4082', icon=github_icon)
class GetIssue(Node):
    def __init__(self):
        super().__init__()

        # Input
        self.in_conn_id = InVariable(
            title='Connection Id',
            type='String',
            scope='Message',
            name='connection_id',
            messageScope=True
        )

        self.in_repo_name = InVariable(
            title='Repository Name',
            type='String',
            scope='Custom',
            name='',
            customScope=True,
            messageScope=True            
        )

        self.in_issue_number = InVariable(
            title='Issue Number',
            type='Integer',
            scope='Custom',
            name='',
            customScope=True,
            messageScope=True            
        )

        # Output
        self.out_issue = OutVariable(
            title='Issue',
            type='Object',
            scope='Message',
            name='issue',
            messageScope=True
        )

    def on_create(self):
        return

    def on_message(self, ctx: Context):
        conn_id = self.in_conn_id.get(ctx)
        repo_name = self.in_repo_name.get(ctx)
        issue_number = self.in_issue_number.get(ctx)

        if not conn_id or not repo_name or not issue_number:
            raise ValueError("Connection Id, Repository Name, and Issue Number cannot be empty")

        github_obj = github_auth_manager.get_github_object(conn_id)
        
        try:
            repo = github_obj.get_repo(repo_name)
            issue = repo.get_issue(number=issue_number)
            self.out_issue.set(ctx, issue)
        except Exception as e:
            raise ValueError(f"Failed to get issue: {e}")

    def on_close(self):
        return
