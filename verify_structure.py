"""Verify VitalSync backend structure"""
import os

required_files = [
    "app/main.py",
    "app/routes/iot_routes.py",
    "app/routes/health_routes.py",
    "app/routes/alert_routes.py",
    "app/controllers/iot_controller.py",
    "app/controllers/health_controller.py",
    "app/controllers/alert_controller.py",
    "app/services/firestore_service.py",
    "app/services/report_service.py",
    "app/services/alert_service.py",
    "app/services/mock_data_service.py",
    "app/schemas/iot_schema.py",
    "app/schemas/alert_schema.py",
    "app/config/firebase.py",
    "app/config/settings.py",
    "app/utils/logger.py",
    "requirements.txt",
    ".env.example",
    "README.md"
]

print("🔍 Verifying VitalSync Backend Structure...\n")

missing = []
for file in required_files:
    if os.path.exists(file):
        print(f"✅ {file}")
    else:
        print(f"❌ {file}")
        missing.append(file)

print("\n" + "="*50)
if not missing:
    print("✅ All required files present!")
    print("🚀 Backend is ready to run!")
    print("\nNext steps:")
    print("1. Add serviceAccountKey.json from Firebase")
    print("2. Run: pip install -r requirements.txt")
    print("3. Run: uvicorn app.main:app --reload")
else:
    print(f"❌ Missing {len(missing)} files")
