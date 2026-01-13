import time
from app.services.digest_service import send_daily_digest

print("📬 Daily digest worker started")

while True:
    send_daily_digest()
    print("✅ Digest sent")
    time.sleep(60 * 60 * 24)  # 24 hours
    
# def send_digest_now():
#     print("🚀 MANUAL DIGEST TRIGGERED")
#     send_daily_digest()
#     print("✅ MANUAL DIGEST FINISHED")
