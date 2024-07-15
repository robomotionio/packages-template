from robomotion.node import Node
from robomotion.decorators import register_node
from robomotion.variable import InVariable, OutVariable
from robomotion.message import Context

from nodes.auth_manager import github_auth_manager
from nodes.icon import github_icon

@register_node(name='Robomotion.GitHub.ListRepos', title='List Repositories', color='#0D4082', icon=github_icon)
class ListRepos(Node):
    def __init__(self):
        super().__init__()

        # Input
        self.in_conn_id = InVariable(
            title='Connection Id',
            type='String',
            scope='Message',
            name='connection_id',
            customScope=True,
            messageScope=True
        )

        # Output
        self.out_repos = OutVariable(
            title='Repositories',
            type='List',
            scope='Message',
            name='repositories',
            messageScope=True
        )

    def on_create(self):
        return

    def on_message(self, ctx: Context):
        conn_id = self.in_conn_id.get(ctx)
        if not conn_id:
            raise ValueError("Connection Id cannot be empty")

        github_obj = github_auth_manager.get_github_object(conn_id)
        
        try:
            repos = [repo.name for repo in github_obj.get_user().get_repos()]
        except Exception as e:
            raise ValueError(f"Failed to list repositories: {e}")

        self.out_repos.set(ctx, repos)

    def on_close(self):
        return
