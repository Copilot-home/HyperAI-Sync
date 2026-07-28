"""
# NOTE: This is a sanitized version for public release
Autonomic Nervous System - HyperAI Biological Architecture
Biological Analog: Hoành cách (Diaphragm) - Điều hòa tự động
Consciousness Layer: 1_unconscious (Reflexes)
Function: Điều khiển reflexes tự động, quản lý tài nguyên
"""

import threading
import time
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional


class AutonomicMode(Enum):
    """Chế độ hoạt động của hệ thống tự động"""

    SYMPATHETIC = "sympathetic"  # Chiến đấu hoặc chạy trốn
    PARASYMPATHETIC = "parasympathetic"  # Nghỉ ngơi và tiêu hóa
    BALANCED = "balanced"  # Cân bằng


class ReflexType(Enum):
    """Các loại reflex tự động"""

    RESOURCE_ALLOCATION = "resource_allocation"
    THREAT_RESPONSE = "threat_response"
    ENERGY_CONSERVATION = "energy_conservation"
    SYSTEM_MAINTENANCE = "system_maintenance"


@dataclass
class AutonomicState:
    """Trạng thái của hệ thống tự động"""

    mode: AutonomicMode
    heart_rate: float  # Tốc độ xử lý
    resource_allocation: Dict[str, float]
    energy_level: float
    stress_level: float
    last_update: float


class AutonomicNervousSystem:
    """
    Hệ thống thần kinh tự động - Điều khiển reflexes tự động
    Biological: Hoành cách (Diaphragm) - Điều hòa tự động
    """

    def __init__(self):
        self.state = AutonomicState(
            mode=AutonomicMode.BALANCED,
            heart_rate=1.0,
            resource_allocation={"cpu": 0.5, "memory": 0.5, "network": 0.3},
            energy_level=1.0,
            stress_level=0.0,
            last_update=time.time(),
        )
        self.reflexes: Dict[ReflexType, bool] = {reflex: False for reflex in ReflexType}
        self.monitoring_thread: Optional[threading.Thread] = None
        self.is_active = False

    def start_autonomic_control(self):
        """Khởi động hệ thống điều khiển tự động"""
        if self.is_active:
            return

        self.is_active = True
        self.monitoring_thread = threading.Thread(target=self._monitor_and_adjust, daemon=True)
        self.monitoring_thread.start()
        print(" Autonomic Nervous System activated - " "Automatic regulation started")

    def stop_autonomic_control(self):
        """Dừng hệ thống điều khiển tự động"""
        self.is_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=1.0)
        print("⏹ Autonomic Nervous System deactivated")

    def _monitor_and_adjust(self):
        """Theo dõi và điều chỉnh tự động"""
        while self.is_active:
            try:
                self._assess_system_state()
                self._trigger_reflexes()
                self._adjust_resources()
                time.sleep(1.0)  # Kiểm tra mỗi giây
            except (RuntimeError, ValueError) as e:
                print(f"⚠ Autonomic monitoring error: {e}")

    def _assess_system_state(self):
        """Đánh giá trạng thái hệ thống"""
        # Giả lập đánh giá dựa trên các chỉ số
        current_time = time.time()
        time_since_update = current_time - self.state.last_update

        # Tăng stress nếu không có cập nhật
        if time_since_update > 5.0:
            self.state.stress_level = min(1.0, self.state.stress_level + 0.1)

        # Giảm năng lượng theo thời gian
        self.state.energy_level = max(0.0, self.state.energy_level - 0.01)

        self.state.last_update = current_time

    def _trigger_reflexes(self):
        """Kích hoạt reflexes dựa trên trạng thái"""
        # Threat response nếu stress cao
        if self.state.stress_level > 0.7:
            self.reflexes[ReflexType.THREAT_RESPONSE] = True
            self.state.mode = AutonomicMode.SYMPATHETIC
            self.state.heart_rate = min(2.0, self.state.heart_rate + 0.2)
        else:
            self.reflexes[ReflexType.THREAT_RESPONSE] = False

        # Energy conservation nếu năng lượng thấp
        if self.state.energy_level < 0.3:
            self.reflexes[ReflexType.ENERGY_CONSERVATION] = True
            self.state.mode = AutonomicMode.PARASYMPATHETIC
        else:
            self.reflexes[ReflexType.ENERGY_CONSERVATION] = False

        # Resource allocation nếu cần
        if any(self.reflexes.values()):
            self.reflexes[ReflexType.RESOURCE_ALLOCATION] = True

    def _adjust_resources(self):
        """Điều chỉnh phân bổ tài nguyên"""
        if self.state.mode == AutonomicMode.SYMPATHETIC:
            # Tăng tài nguyên cho xử lý khẩn cấp
            cpu_alloc = self.state.resource_allocation["cpu"]
            self.state.resource_allocation["cpu"] = min(1.0, cpu_alloc + 0.1)
            mem_alloc = self.state.resource_allocation["memory"]
            self.state.resource_allocation["memory"] = min(1.0, mem_alloc + 0.1)
        elif self.state.mode == AutonomicMode.PARASYMPATHETIC:
            # Giảm tài nguyên để tiết kiệm năng lượng
            cpu_alloc = self.state.resource_allocation["cpu"]
            self.state.resource_allocation["cpu"] = max(0.1, cpu_alloc - 0.05)
            net_alloc = self.state.resource_allocation["network"]
            self.state.resource_allocation["network"] = max(0.1, net_alloc - 0.05)

    def get_status(self) -> Dict:
        """Lấy trạng thái hiện tại của hệ thống"""
        return {
            "mode": self.state.mode.value,
            "heart_rate": self.state.heart_rate,
            "energy_level": self.state.energy_level,
            "stress_level": self.state.stress_level,
            "resource_allocation": self.state.resource_allocation.copy(),
            "active_reflexes": [reflex.value for reflex, active in self.reflexes.items() if active],
            "is_active": self.is_active,
        }

    def manual_override(self, mode: AutonomicMode):
        """Ghi đè thủ công chế độ"""
        self.state.mode = mode
        print(f"🔧 Manual override: Switched to {mode.value} mode")

    def reset_to_balance(self):
        """Đặt lại về trạng thái cân bằng"""
        self.state.mode = AutonomicMode.BALANCED
        self.state.heart_rate = 1.0
        self.state.stress_level = 0.0
        for reflex in self.reflexes:
            self.reflexes[reflex] = False
        print("⚖ System reset to balanced state")


# Global instance
autonomic_system = AutonomicNervousSystem()

if __name__ == "__main__":
    # Demo usage
    system = AutonomicNervousSystem()
    system.start_autonomic_control()

    try:
        for i in range(10):
            status = system.get_status()
            print(f"Status {i}: Mode={status['mode']}, " f"Energy={status['energy_level']:.2f}")
            time.sleep(2)
    except KeyboardInterrupt:
        pass
    finally:
        system.stop_autonomic_control()
