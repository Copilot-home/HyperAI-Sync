#!/usr/bin/env python3
# NOTE: This is a sanitized version for public release
# Core proprietary algorithms have been replaced with placeholders
# -*- coding: utf-8 -*-
"""
HyperAI Phoenix - Demo Tương Tác Bằng Tiếng Việt
===============================================
Demo tương tác để trải nghiệm sức mạnh của 3 agent HyperAI
"""

import asyncio
import os
import sys
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class HyperAIDemoVietnamese:
    """Interactive demo for HyperAI Phoenix in Vietnamese"""

    def __init__(self):
        self.controller = None
        self.demo_history = []
        self._load_system()

    def _load_system(self):
        """Load HyperAI system components"""
        try:
            from unified_agent_controller import UnifiedAgentController

            self.controller = UnifiedAgentController()
            print(" Hệ thống HyperAI Phoenix đã tải thành công!")
        except ImportError as e:
            print(f" Không thể tải hệ thống: {e}")
            self.controller = None

    def show_welcome(self):
        """Display welcome message and system info in Vietnamese"""
        print("\n" + "=" * 70)
        print(" CHÀO MỪNG ĐẾN VỚI HYPERAI PHOENIX - HỆ THỐNG AI TỐI TÂN")
        print("=" * 70)
        print(
            """
 **3 AGENT - 3 CHUYÊN MÔN - 1 HỆ THỐNG THỐNG NHẤT**

 **Agent Ý Thức**: Nhà Sáng Tạo Tầm Nhìn
   • Thiết kế UI/UX & Trải nghiệm Người dùng
   • Giải quyết vấn đề Sáng tạo
   • Trí tuệ Văn hóa & Yếu tố Con người
   • Tầm nhìn Chiến lược & Đổi mới

 **Agent Lý Trí Lượng Tử**: Tối ưu Hóa Logic
   • Tối ưu Thuật toán & Hiệu suất
   • Phân tích Kỹ thuật & Kiến trúc
   • Xử lý Dữ liệu & Phân tích
   • Triển khai Chính xác

 **Agent Doanh Nghiệp**: Người Bảo Vệ Kinh Doanh
   • Bảo mật & Tuân thủ Doanh nghiệp
   • Chiến lược Kinh doanh & Doanh thu
   • Kiến trúc Có thể Mở rộng & Triển khai
   • Đánh giá Rủi ro & Quản trị

 **Định tuyến Thông minh**: Yêu cầu tự động được chuyển đến agent tốt nhất
 **Xử lý Thời gian Thực**: Phản hồi tức thì với điểm tin cậy
 **Giám sát Hiệu suất**: Theo dõi hiệu suất và độ chính xác của agent
        """
        )
        print("=" * 70)

    def show_demo_options(self):
        """Show available demo options in Vietnamese"""
        print("\n🎮 TÙY CHỌN DEMO:")
        print("1.  Test Agent Ý Thức (Sáng tạo/Thiết kế)")
        print("2.  REAL LOGIC NEEDED)")
        print("3.  Test Agent Doanh Nghiệp (Kinh doanh/Bảo mật)")
        print("4.  Test Yêu cầu Hỗn hợp (Tự động định tuyến)")
        print("5.  Xem Thống kê Hệ thống")
        print("6.  Xem Lịch sử Demo")
        print("7. 🚪 Thoát Demo")
        print("\n" + "-" * 50)

    def get_demo_request(self, option: int) -> str:
        """Get sample request based on option in Vietnamese"""
        requests = {
            1: [
                "Thiết kế giao diện ứng dụng di động đẹp và trực quan",
                "Tạo kết nối cảm xúc với người dùng của chúng ta",
                "Phát triển chiến lược thương hiệu sáng tạo cho startup",
                "Cải thiện luồng trải nghiệm người dùng của website",
                "Thêm yếu tố nghệ thuật vào thiết kế sản phẩm",
            ],
            2: [
                "Tối ưu thuật toán sắp xếp để có hiệu suất tốt hơn",
                "Phân tích kiến trúc kỹ thuật của hệ thống",
                "Gỡ lỗi lỗi logic phức tạp trong code",
                "Triển khai pipeline xử lý dữ liệu hiệu quả",
                "Tính độ phức tạp tính toán của thuật toán",
            ],
            3: [
                "Triển khai các biện pháp bảo mật doanh nghiệp",
                "Phát triển chiến lược kinh doanh để mở rộng thị trường",
                "Đảm bảo tuân thủ các quy định ngành",
                "Tối ưu hóa luồng doanh thu và lợi nhuận",
                "Đánh giá rủi ro kinh doanh và chiến lược giảm thiểu",
            ],
            4: [
                "Thiết kế hệ thống xác thực an toàn và thân thiện",
                "Tạo nền tảng thương mại điện tử hiệu suất cao",
                "Phát triển bảng điều khiển trí tuệ kinh doanh AI",
                "Xây dựng kiến trúc đám mây có thể mở rộng với giám sát",
                "Triển khai chiến dịch marketing sáng tạo với phân tích",
            ],
        }

        if option in requests:
            import random

            return random.choice(requests[option])
        return ""

    async def process_demo_request(self, user_input: str):
        """Process a demo request"""
        if not self.controller:
            print(" Hệ thống chưa tải")
            return

        print(f"\n Đang xử lý: '{user_input}'")
        print(" Đang phân tích yêu cầu...")

        try:
            # Process request
            response = await self.controller.process_request(user_input)

            # Store in history
            self.demo_history.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "request": user_input,
                    "agent": response.agent_type,
                    "confidence": response.confidence_score,
                    "response": (response.response_content[:200] + "..." if len(response.response_content) > 200 else response.response_content),
                }
            )

            # Display results
            print(f"\n **PHÂN CÔNG CHO: AGENT {response.agent_type.upper()}**")
            print(f" **ĐIỂM TIN CẬY: {response.confidence_score:.2f}**")
            print(f"⏱ **THỜI GIAN XỬ LÝ: {response.processing_time:.2f}s**")
            print(f"\n💬 **PHẢN HỒI:**\n{response.response_content}")
            print("\n" + "-" * 70)

        except Exception as e:
            print(f" Lỗi xử lý yêu cầu: {e}")

    def show_statistics(self):
        """Show system statistics in Vietnamese"""
        if not self.demo_history:
            print(" Chưa có lịch sử demo")
            return

        print("\n THỐNG KÊ DEMO")
        print("=" * 50)

        total_requests = len(self.demo_history)
        agent_counts = {}
        confidence_sum = 0

        for item in self.demo_history:
            agent = item["agent"]
            agent_counts[agent] = agent_counts.get(agent, 0) + 1
            confidence_sum += item["confidence"]

        print(f"Tổng yêu cầu đã xử lý: {total_requests}")
        print(".2f")

        print("\n Phân bổ Agent:")
        for agent, count in agent_counts.items():
            percentage = (count / total_requests) * 100
            print(f"   {agent}: {count} ({percentage:.1f}%)")

        print("\n Hoạt động Gần đây:")
        for i, item in enumerate(self.demo_history[-5:], 1):
            print(f"{i}. [{item['agent']}] {item['request'][:50]}...")

    def show_history(self):
        """Show demo history in Vietnamese"""
        if not self.demo_history:
            print(" Chưa có lịch sử demo")
            return

        print("\n LỊCH SỬ DEMO")
        print("=" * 50)

        for i, item in enumerate(self.demo_history, 1):
            print(f"\n{i}. **{item['timestamp'][:19]}**")
            print(f"    Yêu cầu: {item['request']}")
            print(f"    Agent: {item['agent']} (điểm tin cậy: {item['confidence']:.2f})")
            print(f"   💬 Phản hồi: {item['response']}")

    async def run_interactive_demo(self):
        """Run the interactive demo in Vietnamese"""
        self.show_welcome()

        while True:
            self.show_demo_options()

            try:
                choice = input(" Chọn tùy chọn (1-7): ").strip()

                if choice == "7":
                    print("\n Cảm ơn bạn đã khám phá HyperAI Phoenix!")
                    print(" Hệ thống đã sẵn sàng cho sử dụng thực tế!")
                    break

                elif choice == "5":
                    self.show_statistics()
                    input("\n⏎ Nhấn Enter để tiếp tục...")

                elif choice == "6":
                    self.show_history()
                    input("\n⏎ Nhấn Enter để tiếp tục...")

                elif choice in ["1", "2", "3", "4"]:
                    option = int(choice)

                    # Get demo request
                    demo_request = self.get_demo_request(option)
                    if demo_request:
                        print(f"\n Yêu cầu Demo: '{demo_request}'")
                        use_demo = input("Sử dụng yêu cầu demo này? (y/n): ").strip().lower()

                        if use_demo == "y":
                            await self.process_demo_request(demo_request)
                        else:
                            custom_request = input("Nhập yêu cầu tùy chỉnh: ").strip()
                            if custom_request:
                                await self.process_demo_request(custom_request)
                    else:
                        custom_request = input("Nhập yêu cầu của bạn: ").strip()
                        if custom_request:
                            await self.process_demo_request(custom_request)

                    input("\n⏎ Nhấn Enter để tiếp tục...")

                else:
                    print(" Tùy chọn không hợp lệ. Vui lòng chọn 1-7.")

            except KeyboardInterrupt:
                print("\n Tạm biệt!")
                break
            except Exception as e:
                print(f" Lỗi: {e}")
                input("\n⏎ Nhấn Enter để tiếp tục...")


def main():
    """Main demo function"""
    print(" Khởi động Demo Tương tác HyperAI Phoenix...")

    demo = HyperAIDemoVietnamese()

    if not demo.controller:
        print(" Không thể khởi động demo - hệ thống chưa tải")
        return

    # Run interactive demo
    asyncio.run(demo.run_interactive_demo())


if __name__ == "__main__":
    main()
