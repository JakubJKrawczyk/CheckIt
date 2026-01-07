import os

# Runtime hook executed by PyInstaller before your app starts.
# Sets default update URL unless user provided their own.
os.environ.setdefault("CHECKIT_UPDATE_URL", "https://apps.jakubkrawczyk.com/checkit")
