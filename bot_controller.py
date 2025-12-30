# simple_check.py
from info import handle_bot_command

# শুধু র‍্যাক রেজাল্ট দেখি
result = handle_bot_command("/info bd 3999072239")
print("API রেসপন্স:")
print("="*50)
print(result)
print("="*50)
print(f"লেংথ: {len(result)} characters")
print(f"প্রথম 10 chars: '{result[:10]}'")