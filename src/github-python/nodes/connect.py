from robomotion.node import Node
from robomotion.decorators import register_node
from robomotion.variable import OutVariable, Credentials, VaultItemCategory
from robomotion.message import Context

from common import api_key_store
from icon import github_icon

@register_node(name='Robomotion.GitHub.Connect', title='Connect', color='#0D4082', icon=github_icon)
class Connect(Node):
    def __init__(self):
        super().__init__()

        # Output
        self.out_conn_id = OutVariable(
            title='Connection Id', 
            type='String', 
            scope='Message', 
            name='connection_id', 
            messageScope=True
        )

        # Options
        self.opt_api_key = Credentials(
            title='API Key', 
            category=VaultItemCategory.Token
        )

    def on_create(self):
        return

    def on_message(self, ctx: Context):

        vault_item = self.opt_api_key.get_vault_item(ctx)
        if "value" not in vault_item:
            raise ValueError("Not an API Key item")
        
        api_key = vault_item["value"]
        if not api_key:
            raise ValueError("API Key cannot be empty")
        
        conn_id = api_key_store.add_api_key(api_key)
        
        self.out_conn_id.set(ctx, conn_id)

    def on_close(self):
        return
