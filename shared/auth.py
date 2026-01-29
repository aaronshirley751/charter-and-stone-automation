import os
import msal
from pathlib import Path
from dotenv import load_dotenv

# Load env from the project root
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../"))
load_dotenv(os.path.join(project_root, ".env"))

AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
TOKEN_CACHE_PATH = Path.home() / ".charterstone" / "token_cache.json"

class GraphAuthenticator:
    """
    Centralized Authentication Handler for all Charter & Stone Agents.
    Uses MSAL Device Code Flow and local caching.
    """
    def __init__(self):
        self._token_cache = msal.SerializableTokenCache()
        self._load_token_cache()
        self._app = msal.PublicClientApplication(
            AZURE_CLIENT_ID,
            authority=f"https://login.microsoftonline.com/{AZURE_TENANT_ID}",
            token_cache=self._token_cache
        )
    
    def _load_token_cache(self):
        if TOKEN_CACHE_PATH.exists():
            self._token_cache.deserialize(TOKEN_CACHE_PATH.read_text())
            
    def _save_token_cache(self):
        TOKEN_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        TOKEN_CACHE_PATH.write_text(self._token_cache.serialize())
    
    def get_access_token(self):
        accounts = self._app.get_accounts()
        scopes = ["Tasks.ReadWrite", "Group.Read.All", "User.Read"]
        
        # 1. Try Silent (Cache)
        if accounts:
            result = self._app.acquire_token_silent(scopes=scopes, account=accounts[0])
            if result and "access_token" in result:
                self._save_token_cache()
                return result["access_token"]
        
        # 2. Device Code Flow (Interactive)
        flow = self._app.initiate_device_flow(scopes=scopes)
        if "user_code" not in flow:
            print("❌ Auth: Failed to create device flow")
            return None
            
        print(f"\n⚠️ AUTH REQUIRED: {flow['message']}")
        result = self._app.acquire_token_by_device_flow(flow)
        
        if "access_token" in result:
            self._save_token_cache()
            return result["access_token"]
        else:
            print(f"❌ Auth Failed: {result.get('error_description')}")
            return None

def get_graph_headers():
    auth = GraphAuthenticator()
    token = auth.get_access_token()
    if token:
        return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    return None
