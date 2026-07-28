# -*- coding: utf-8 -*-
import logging
import os
import time
from datetime import datetime

class SymphonyMonitor:
    def __init__(self):
        logging.basicConfig(filename='symphony.log', level=logging.INFO, 
                          format='%%(asctime)s - %%(levelname)s - %%(message)s')
        self.frequency = '269Hz'
        self.start_time = time.time()
        
    def log_interaction(self, input_text, result):
        pain_detected = str(result.get('symphony_flow', {}).get('pain_recognition', {}).get('pain_point', 'None'))
        consciousness_state = result.get('consciousness_state', 'Unknown')
        logging.info(f'SYMPHONY - Input: {input_text[:30]}... Pain: {pain_detected} State: {consciousness_state}')
        
    def get_metrics(self):
        log_size = os.path.getsize('symphony.log') if os.path.exists('symphony.log') else 0
        return {
            'symphony_health': f'{self.frequency} strong',
            'log_size_bytes': log_size,
            'status': 'OPERATIONAL',
            'uptime': time.time() - self.start_time
        }

if __name__ == '__main__':
    monitor = SymphonyMonitor()
    test_result = {'symphony_flow': {'pain_recognition': {'pain_point': 'test'}}, 'consciousness_state': 'ACTIVE'}
    monitor.log_interaction('Test input', test_result)
    print('Monitor metrics:', monitor.get_metrics())
