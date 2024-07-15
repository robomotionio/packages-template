from robomotion.node import Node
from robomotion.decorators import register_node
from robomotion.variable import InVariable, OutVariable, Variable
from robomotion.message import Context

from nodes.auth_manager import github_auth_manager
from nodes.icon import github_icon

@register_node(name='Robomotion.GitHub.Repository.SearchRepos', title='Search Repositories', color='#0D4082', icon=github_icon)
class SearchRepos(Node):
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

        self.in_query = Variable(
            title='Query',
            type='String',
            scope='Custom',
            name='',
            customScope=True,
            messageScope=True            
        )

        # Output
        self.out_repos = OutVariable(
            title='Repositories',
            type='Object',
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

        query = self.in_query.get(ctx)
        if not query:
            raise ValueError("Query cannot be empty")

        github_obj = github_auth_manager.get_github_object(conn_id)
        
        try:
            repositories = github_obj.search_repositories(query=query)
            repos = [repo.full_name for repo in repositories]
        except Exception as e:
            raise ValueError(f"Failed to search repositories: {e}")

        self.out_repos.set(ctx, repos)

    def on_close(self):
        return
