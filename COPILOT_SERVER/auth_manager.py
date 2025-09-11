# -*- coding: utf-8 -*-
# auth_manager.py - Simple JWT Auth for Empathy Symphony
#  Secure empathy flow với Vietnamese soul authentication

import secrets
from datetime import datetime, timedelta

class AuthManager:
    def __init__(self):
        # Demo users with Vietnamese empathy context
        self.users = {
            'admin': 'empathy269',
            'enterprise': 'vietnam_soul'
        }
        self.tokens = {}  # {token: {user, expiry, frequency}}
        
    def login(self, username, password):
        ''' Vietnamese empathy authentication'''
        if username in self.users and self.users[username] == password:
            token = secrets.token_hex(16)
            expiry = datetime.now() + timedelta(hours=1)
            self.tokens[token] = {
                'user': username, 
                'expiry': expiry,
                'frequency': '269Hz Vietnamese Soul Access'
            }
            return {
                'access_token': token,
                'status': 'Authenticated with 269Hz empathy ',
                'user': username,
                'frequency': '269Hz access granted',
                'message': 'Welcome to Vietnamese Cultural Bridge!'
            }
        return {'error': 'Invalid credentials - Empathy access denied'}

    def verify_token(self, token):
        ''' Verify empathy authentication token'''
        if token in self.tokens:
            token_data = self.tokens[token]
            if token_data['expiry'] > datetime.now():
                return {
                    'user': token_data['user'], 
                    'valid': True,
                    'frequency': token_data['frequency']
                }
            else:
                # Token expired, clean up
                del self.tokens[token]
        return {'valid': False, 'error': 'Token invalid or expired'}
        
    def get_active_sessions(self):
        ''' Get active empathy sessions'''
        active = []
        current_time = datetime.now()
        for token, data in list(self.tokens.items()):
            if data['expiry'] > current_time:
                active.append({
                    'user': data['user'],
                    'expires_in': str(data['expiry'] - current_time),
                    'frequency': data['frequency']
                })
            else:
                del self.tokens[token]
        return {'active_sessions': active, 'total': len(active)}

# Test Auth Manager
if __name__ == '__main__':
    print(' AUTH MANAGER - Vietnamese Soul Authentication')
    auth = AuthManager()
    
    # Test login
    login_result = auth.login('admin', 'empathy269')
    print('Login Test:', login_result)
    
    if 'access_token' in login_result:
        token = login_result['access_token']
        verify_result = auth.verify_token(token)
        print('Verification Test:', verify_result)
        
        sessions = auth.get_active_sessions()
        print('Active Sessions:', sessions)
    
    print(' Auth Manager Ready for Symphony Integration!')
