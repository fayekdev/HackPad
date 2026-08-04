from backend.profile_manager import ProfileManager
from backend.action_runner import ActionRunner

pm = ProfileManager()
runner = ActionRunner(pm)

print("Running key_1...")
runner.run_button("key_5")

