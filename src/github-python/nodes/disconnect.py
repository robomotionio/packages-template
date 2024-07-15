from robomotion.node import Node
from robomotion.decorators import register_node
from robomotion.variable import InVariable
from robomotion.message import Context

from nodes.auth_manager import github_auth_manager
from nodes.icon import github_icon

@register_node(name='Robomotion.GitHub.Disconnect', title='Disconnect', color='#0D4082', icon=github_icon)
class Disconnect(Node):
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

    def on_create(self):
        return

    def on_message(self, ctx: Context):

        conn_id = self.in_conn_id.get(ctx)
        if not conn_id:
            raise ValueError("Connection Id cannot be empty")

        github_auth_manager.delete_github_object(conn_id)

    def on_close(self):
        return
